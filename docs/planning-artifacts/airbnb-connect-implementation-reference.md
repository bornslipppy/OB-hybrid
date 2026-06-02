---
title: "Airbnb Connect Step — Prototype Implementation Reference"
---

# Airbnb Connect Step — Prototype Implementation Reference

**Audience:** Agent building the Guesty Pro Onboarding Wizard prototype  
**Source codebase:** `abnb-distribution-page-master` (provided as ZIP)  
**Companion spec:** `docs/planning-artifacts/ux-design-specification-2026-05-25.md` → section "Airbnb Connect Step — Pre-Built Component Reference"

---

## 0. Critical Rules (Read Before Anything Else)

### Rule 1 — Never modify the source codebase

Every file listed under "REUSE" in section 2 must be **copied into the prototype project** at `src/prototype/connect/` (or equivalent). Never edit files inside `abnb-distribution-page-master` itself — that is a production codebase. All mocks and modifications described below apply to the copies in the prototype project only.

### Rule 2 — Prototype-only mocks must never ship to production

The mocks in this document bypass real OAuth, return hardcoded listings, and accept any selection. If any of this code reaches production, OAuth security is silently broken.

Gate every mock with a build-time guard. Recommended pattern:

```ts
// At top of every mock file:
if (process.env.NODE_ENV === 'production' && process.env.REACT_APP_PROTOTYPE !== 'true') {
  throw new Error('Prototype mock loaded in production build. This is a fatal misconfiguration.');
}
```

Alternative: place the entire `prototype/` directory behind a build exclusion in `tsconfig.json` and the bundler config.

---

## 1. What You Are Building

S1 of the onboarding wizard is a 2-step Airbnb connection sub-flow. You do **not** build it from scratch. You lift the pre-built components from `abnb-distribution-page-master`, apply a thin prototype mock layer to skip real OAuth, and embed them inside the onboarding wizard shell.

The result: user clicks "Pre-connect to Airbnb" → 1.5s loading state → listing selection screen with 8 dummy listings → user clicks "Select listings" → AHA canvas reveal fires.

---

## 2. Source Component Map

All paths are relative to `abnb-distribution-page-master/src/`.

```
app/views/bulk-import/
  BulkImport.tsx                    ← DO NOT reuse (has WizardWrapper chrome)
  components/
    BulkImportWizard.tsx            ← DO NOT reuse as outer wizard
    ConnectAbnb.tsx                 ← REUSE — mock the hook + remove useEffect
    ImportListings.tsx              ← REUSE — replace API logic with dummy data
    ImportListingsContent.tsx       ← REUSE AS-IS
    ImportListingsSubheader.tsx     ← REUSE AS-IS
    ImportListingsLoader.tsx        ← NOT NEEDED in prototype (no async loading)

app/components/
    listings/
      ListingsFilter.tsx            ← REUSE AS-IS
      ListingsList.tsx              ← REUSE AS-IS
      ListingItem.tsx               ← REUSE AS-IS
      SelectListingsSkeleton.tsx    ← NOT NEEDED in prototype

app/hooks/
    useIdListContext.tsx            ← REUSE AS-IS (selection state management)
    useContainerHeight.ts           ← REUSE AS-IS (virtual list height calc)
    useHistoryPush.ts               ← REUSE AS-IS

app/api/hooks/
    useGetPreConnectAccount.ts      ← DO NOT use — replaced by mock
    useFetchLastIntegration.ts      ← DO NOT use — replaced by dummy data
    useIntegrationListings.ts       ← DO NOT use — replaced by dummy data
    useImportListings.ts            ← KEEP but intercept onSuccess to call onConnected

constants/
    filterKeys.ts                   ← REUSE AS-IS
    filterTypes.ts                  ← REUSE AS-IS
    listingPublishTypes.ts          ← REUSE AS-IS
    hostRole.ts                     ← REUSE AS-IS

types/
    listing.ts                      ← REUSE AS-IS (Listing interface)
    index.ts                        ← REUSE AS-IS
```

---

## 3. Required Dependencies

Copy these from `abnb-distribution-page-master/package.json` into the prototype project:

```json
{
  "@guestyci/arc": "1.8.1",
  "@guestyci/arc-styles": "1.2.1",
  "@guestyci/localize": "^4.1.11",
  "@tanstack/react-query": "^4.36.1",
  "react-router-dom": "^5.1.2",
  "lucide-react": "^0.545.0",
  "react-virtuoso": "^4.14.1",
  "react-hook-form": "7.25.3",
  "classnames": "^2.2.6",
  "lodash": "^4.17.15"
}
```

**Not needed for the prototype** (all API calls are mocked):
- `@guestyci/agni`
- `@guestyci/feature-toggle-fe`
- `axios`

**Arc Styles setup** — in the prototype's entry CSS, import Arc styles:
```css
@import '@guestyci/arc-styles/dist/index.css';
```

And on the `<html>` element, add the `gst-` prefix class and optionally `dark` for dark mode:
```html
<html class="gst-font-sans">
```

---

## 4. Mock: ConnectAbnb (Step 1)

Replace the real hook with a timed mock. The existing JSX, copy, and Arc components stay unchanged.

**Original `ConnectAbnb.tsx` — lines to replace:**

```tsx
// REMOVE these imports:
import useGetPreConnectAccount from 'app/api/hooks/useGetPreConnectAccount';
import { DOMAIN } from 'constants/domain';

// REMOVE the useEffect that watches integrationId:
useEffect(() => {
  if (integrationId && activeStep?.id === 'connect') {
    goNext();
  }
}, [integrationId, activeStep, goNext]);

// REMOVE the real handler:
const { mutateAsync: connectAccount, isLoading } = useGetPreConnectAccount({ onError });
const onPreconnectClick = async () => { ... };
```

**Replace with:**

```tsx
import { useState } from 'react';

// Inside ConnectAbnb component:
const [isLoading, setIsLoading] = useState(false);

const onPreconnectClick = () => {
  setIsLoading(true);
  setTimeout(() => {
    setIsLoading(false);
    goNext();
  }, 1500); // simulates redirect + OAuth callback round-trip
};
```

Also remove the `integrationId` / `action` / `errorMessage` reads from `searchParams` — they are only relevant for the real OAuth callback. The `errorMessage` Alert at the bottom of the JSX can be removed too.

**Final simplified ConnectAbnb interface for prototype:**

This version supports demoing the OAuth failure state (DC-8 FAILED, UJ-7) via a URL flag: `?mockError=oauth-failed | scope-rejected | network`.

```tsx
import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Heading, Text, Button, Stack, Alert, AlertTitle, useWizard } from '@guestyci/arc';
import t from '@guestyci/localize/t.macro';

const ERROR_COPY: Record<string, string> = {
  'oauth-failed': "Your Airbnb session may have expired. Try signing in again.",
  'scope-rejected': "Looks like permission wasn't granted. We only need view-access.",
  'network': "Airbnb didn't respond. Try again?",
};

const ConnectAbnb = () => {
  const { goNext } = useWizard();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(false);
  const [errorKey, setErrorKey] = useState<string | null>(null);

  // Read mock error flag once on mount
  const mockError = new URLSearchParams(location.search).get('mockError');

  const onPreconnectClick = () => {
    if (isLoading) return; // double-click guard
    setIsLoading(true);
    setErrorKey(null);
    setTimeout(() => {
      setIsLoading(false);
      if (mockError && ERROR_COPY[mockError]) {
        setErrorKey(mockError);
      } else {
        goNext();
      }
    }, 1500);
  };

  return (
    <Container data-qa="bulk-import-step-1" className="gst-overflow-auto">
      <Heading className="gst-mb-2" variant="h2">
        {t('Airbnb listings to be imported')}
      </Heading>
      <Text className="gst-text-muted-foreground">
        {t('A view-only connection will import data without making changes to your listings on Airbnb.')}
      </Text>
      <Text bold className="gst-text-muted-foreground gst-pt-14">
        {t('Start test-driving Guesty:')}
      </Text>
      <Text size="base" className="gst-text-muted-foreground">
        {t("Test Guesty without affecting your listings on Airbnb. The property management software you're")}
        <br />
        {t('using will still be connected to Airbnb until you decide to switch to Guesty.')}
      </Text>
      <Text size="base" className="gst-text-muted-foreground gst-mt-6">
        {t("We'll import real data from Airbnb so you can explore Guesty. We won't sync changes in Guesty to")}
        <br />
        {t('Airbnb until you are ready to switch to Guesty and fully connect the Airbnb account.')}
      </Text>
      <Stack spacing={2} className="gst-mt-16">
        <Button
          className="gst-w-fit"
          onClick={onPreconnectClick}
          isLoading={isLoading}
          disabled={isLoading}
        >
          {t('Pre-connect to Airbnb')}
        </Button>
        {errorKey && (
          <Alert variant="critical" dismissible={false}>
            <AlertTitle className="gst-font-normal">{t(ERROR_COPY[errorKey])}</AlertTitle>
          </Alert>
        )}
      </Stack>
    </Container>
  );
};
```

**Demo URLs:**
- `/prototype/wizard?step=connect` — happy path
- `/prototype/wizard?step=connect&mockError=oauth-failed` — token expired
- `/prototype/wizard?step=connect&mockError=scope-rejected` — user denied view-only scope
- `/prototype/wizard?step=connect&mockError=network` — Airbnb unreachable

---

## 5. Mock: ImportListings (Step 2)

Replace the polling + API logic with direct dummy data. The dataset is switchable via URL flag `?mockData=default | empty | inactive` so the prototype can demo DC-9 branches (B1 zero listings, B2 all inactive, B5 first-time host).

**Replace `prototype/connect/ImportListings.tsx` entirely with:**

```tsx
import { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { Container } from '@guestyci/arc';
import ImportListingsContent from 'prototype/connect/ImportListingsContent';
import {
  DUMMY_LISTINGS_EIGHT,
  DUMMY_LISTINGS_EMPTY,
  DUMMY_LISTINGS_INACTIVE,
} from 'prototype/dummyListings';

interface ImportListingsProps {
  onConnected: (selectedIds: string[]) => void;
}

const ImportListings = ({ onConnected }: ImportListingsProps) => {
  const location = useLocation();
  const mockData = new URLSearchParams(location.search).get('mockData') || 'default';

  const listings = useMemo(() => {
    switch (mockData) {
      case 'empty': return DUMMY_LISTINGS_EMPTY;
      case 'inactive': return DUMMY_LISTINGS_INACTIVE;
      default: return DUMMY_LISTINGS_EIGHT;
    }
  }, [mockData]);

  const uniqCities = useMemo(
    () => Array.from(new Set(listings.map((l) => l.city).filter(Boolean))) as string[],
    [listings],
  );

  return (
    <Container data-qa="bulk-import-step-2" className="gst-h-full">
      <ImportListingsContent
        data={{ listings, uniqCities }}
        integrationId="mock-integration-id"
        onConnected={onConnected}
      />
    </Container>
  );
};

export default ImportListings;
```

**Modify `prototype/connect/ImportListingsContent.tsx`** (the copy in the prototype directory — never the original):

Required changes — apply each one exactly:

**a. Add the `onConnected` prop:**
```tsx
interface ImportListingsContentProps {
  data?: { listings: Listing[]; uniqCities: string[] };
  integrationId: string;
  onConnected: (selectedIds: string[]) => void; // ADD THIS
}
```

**b. Seed the selection set with all listings on mount** (the production code starts with empty `idSet`, but the screenshots show "Select all" pre-checked):
```tsx
import { useEffect } from 'react';

// Inside the component body, after the useIdListContext call:
const { idSet, addId } = useIdListContext({ initialData: listings });
useEffect(() => {
  listings.forEach((l) => addId(l.listingIdentifier));
}, [listings, addId]);
```
Verify the exact `useIdListContext` API in `src/app/hooks/useIdListContext.tsx` — if it exposes a different setter (e.g. `setIds(new Set(...))`), use that instead.

**c. Remove these imports and references entirely:**
- `import useImportListings from 'app/api/hooks/useImportListings';`
- `import useHistoryPush from 'app/hooks/useHistoryPush';`
- `import SuccessFlowModal from 'app/components/dialogs/SuccessFlowModal';`
- The `useImportListings` hook call
- The `useEffect` that watches `isListingsImportSuccess`
- The `redirectURL` memo and the `SuccessFlowModal` JSX block

**d. Replace `handleSubmit` with the onConnected call:**
```tsx
const handleSubmit = useCallback(() => {
  onConnected(Array.from(idSet));
}, [idSet, onConnected]);
```

**e. Fix the two button attributes that referenced the removed loading state** — find this Button:
```tsx
<Button
  onClick={handleSubmit}
  disabled={isListingsImportLoading || !idSet.size}
  isLoading={isListingsImportLoading}
>
```
Replace with:
```tsx
<Button
  onClick={handleSubmit}
  disabled={!idSet.size}
>
```

**f. Optional realism delay** — if you want the prototype to feel less instantaneous, wrap the data pass with a brief loader. Add at the top of `ImportListings.tsx`:
```tsx
const MOCK_LOAD_MS = 800; // set to 0 to disable
```
And conditionally render `ImportListingsLoader` for that duration before the content. Keep this off by default; turn on only for demo realism.

---

## 6. Dummy Listings Data

Create `src/prototype/dummyListings.ts` with three exports — one per DC-9 branch the prototype needs to demo. The `image` field is omitted from all entries so `ListingItem` uses its built-in fallback. If you want real thumbnails, commit static images to `public/listing-images/` and reference them as local paths — do NOT use fabricated CDN URLs, they will 404.

```ts
import { Listing } from 'types';

// DC-9 default — UJ-1 Maya happy path (8 listings, 4 cities, 1 inactive, 1 co-host)
export const DUMMY_LISTINGS_EIGHT: Listing[] = [
  {
    listingIdentifier: 'mock-1',
    listingId: 'airbnb-901234',
    name: 'Sunny Studio in South Beach',
    nickname: 'South Beach Studio',
    propertyType: 'Apartment',
    address: '1200 Ocean Dr, Miami Beach, FL 33139',
    city: 'Miami',
    isListed: true,
    status: 'active',
    hostRole: 'owner',
  },
  {
    listingIdentifier: 'mock-2',
    listingId: 'airbnb-901235',
    name: 'Modern 2BR with Pool View',
    nickname: 'Brickell Pool Suite',
    propertyType: 'Apartment',
    address: '801 Brickell Bay Dr, Miami, FL 33131',
    city: 'Miami',
    isListed: true,
    status: 'active',
    hostRole: 'owner',
  },
  {
    listingIdentifier: 'mock-3',
    listingId: 'airbnb-901236',
    name: 'Cozy Loft in Wynwood',
    nickname: 'Wynwood Art Loft',
    propertyType: 'Loft',
    address: '274 NW 26th St, Miami, FL 33127',
    city: 'Miami',
    isListed: true,
    status: 'active',
    hostRole: 'owner',
  },
  {
    listingIdentifier: 'mock-4',
    listingId: 'airbnb-901237',
    name: 'Spacious Villa with Garden',
    nickname: 'Coral Gables Villa',
    propertyType: 'Villa',
    address: '3 Tahiti Beach Island Rd, Coral Gables, FL 33143',
    city: 'Miami',
    isListed: false,
    status: 'inactive',
    hostRole: 'owner',
  },
  {
    listingIdentifier: 'mock-5',
    listingId: 'airbnb-901238',
    name: 'Penthouse with City Views',
    nickname: 'El Poblado Penthouse',
    propertyType: 'Apartment',
    address: 'Calle 10 #43-22, El Poblado, Medellín',
    city: 'Medellin',
    isListed: true,
    status: 'active',
    hostRole: 'co-host',
  },
  {
    listingIdentifier: 'mock-6',
    listingId: 'airbnb-901239',
    name: 'Historic Apartment in Alfama',
    nickname: 'Alfama Heritage',
    propertyType: 'Apartment',
    address: 'R. de São Pedro, 1100-522 Lisboa, Portugal',
    city: 'Lisbon',
    isListed: true,
    status: 'active',
    hostRole: 'owner',
  },
  {
    listingIdentifier: 'mock-7',
    listingId: 'airbnb-901240',
    name: 'Beachfront Casita',
    nickname: 'Barcelona Beachfront',
    propertyType: 'House',
    address: 'Passeig Marítim de la Barceloneta, 08003 Barcelona',
    city: 'Barcelona',
    isListed: true,
    status: 'active',
    hostRole: 'owner',
  },
  {
    listingIdentifier: 'mock-8',
    listingId: 'airbnb-901241',
    name: 'Gothic Quarter Studio',
    nickname: 'Gothic Studio',
    propertyType: 'Apartment',
    address: 'Carrer dels Escudellers, 08002 Barcelona',
    city: 'Barcelona',
    isListed: true,
    status: 'active',
    hostRole: 'owner',
  },
];

// DC-9 B1 — Zero listings (first-time host, B5 also routes here)
export const DUMMY_LISTINGS_EMPTY: Listing[] = [];

// DC-9 B2 — All listings inactive (account exists, nothing live)
export const DUMMY_LISTINGS_INACTIVE: Listing[] = DUMMY_LISTINGS_EIGHT.map((l) => ({
  ...l,
  isListed: false,
  status: 'inactive',
}));
```

> **Note on AHA reveal values:** The reservation count, message count, and canvas banner copy are the wizard shell's responsibility (canvas reveal), not the connect step's. The connect step's contract ends at `onConnected(selectedIds)`. Those values belong in the canvas/AHA reference, not here.

---

## 7. Embedding in the Onboarding Wizard Shell

The onboarding wizard has its own `AppShell` (40/60 split). The Airbnb connect sub-flow occupies the **left panel only**. The right panel (canvas) is owned by the wizard shell.

```tsx
// Inside the onboarding wizard's S1 screen component:

import { Wizard, WizardStepData } from '@guestyci/arc';
import { IdListProvider } from 'app/hooks/useIdListContext';
import ConnectAbnb from './connect/ConnectAbnb.mock';
import ImportListings from './connect/ImportListings.mock';

interface AirbnbConnectStepProps {
  onConnected: (selectedIds: string[]) => void;
}

const AirbnbConnectStep = ({ onConnected }: AirbnbConnectStepProps) => {
  const steps: WizardStepData[] = [
    {
      id: 'connect',
      label: 'Set up a view-only connection',
      content: <ConnectAbnb />,
    },
    {
      id: 'import',
      label: 'Import listings',
      content: <ImportListings onConnected={onConnected} />,
    },
  ];

  return (
    <IdListProvider>
      <Wizard
        steps={steps}
        disableStepNavigation={true}
        showBackButton={false}
        showNextButton={false}
      />
    </IdListProvider>
  );
};
```

The wizard shell calls `onConnected` → advances the outer onboarding wizard to S2 → fires the AHA canvas reveal.

### Bot Alert (DD-5 anchor screen)

The pre-built `ConnectAbnb` does not include the bot advisory. Per the UX spec's DD-5 direction, the **wizard shell** (not this connect-step reference) adds a bot Alert above the step content for sub-step 1. The full anchor-screen bot pattern is owned by the wizard shell spec.

Connect-step-specific copy to use:

> *"We only request view-only access — Guesty reads your listings but never changes them, messages guests, or accepts bookings on Airbnb's side."*

The wizard shell composes this copy into an Arc `Alert variant="information"` with the bot persona. Concrete component composition is the wizard shell's responsibility; verify exact `Alert` slot API and any persona/avatar conventions against the Arc Storybook at `https://livebook.guesty.com/nebula/` before implementing.

---

## 8. Do Not Change List

| File | Reason |
|------|--------|
| `ImportListingsContent.tsx` filter logic | Correctly filters dummy data by city, status, hostRole, search |
| `ListingsFilter.tsx` | Arc Combobox wiring is correct |
| `ListingsList.tsx` | `react-virtuoso` virtual list handles any data size |
| `ListingItem.tsx` | Renders `Listing` interface correctly |
| `useIdListContext.tsx` | Selection state logic is correct |
| All `gst-` CSS class prefixes | Arc Styles Tailwind utilities — never replace with raw Tailwind or inline styles |
| `filterKeys.ts`, `filterTypes.ts`, `listingPublishTypes.ts` | Constants used inside filter logic |

---

## 9. Quick Reference: Mock Flow Summary

```
User clicks "Pre-connect to Airbnb"
  → Button disabled + isLoading state (Arc spinner) — double-click guarded
  → setTimeout(1500ms)
  → If ?mockError flag set: render <Alert variant="critical"> with error copy
    Else: goNext() fires → Arc Wizard advances to sub-step 2

Sub-step 2 mounts
  → Dataset selected by ?mockData flag (default | empty | inactive)
  → DUMMY_LISTINGS_EIGHT (8 items) passed directly to ImportListingsContent
  → useEffect seeds idSet with all listing IDs → "Select all" checked, button enabled
  → Filters: City (derived from listings), Status, Ownership
  → "Showing N listings"

User clicks "Select listings"
  → handleSubmit calls onConnected(Array.from(idSet))
  → Connect step contract ends here
  → Wizard shell (separate component) owns AHA canvas reveal
```
