# Changelog

## 0.4.0
 * Write all datetime fields as iso8601 date-times instead of epoch milliseconds [#25](https://github.com/singer-io/tap-lever/pull/25)

## 0.3.1
 * Add opportunityId (injected by the tap), approved, posting, sentDocument, signedDocument, signatures.candidate
 to opportunity_offers schema [#23](https://github.com/singer-io/tap-lever/pull/23)

## 0.3.0
 * Bookmark on page offset for opportunity sync [#20](https://github.com/singer-io/tap-lever/pull/20)
 * Fix error during sync if no catalog passed in

## 0.2.1
 * Write schema messages when swapping to a new stream [#18](https://github.com/singer-io/tap-lever/pull/18)

## 0.2.0
 * Move Opportunity's substreams into the sync for Opportunity [#16](https://github.com/singer-io/tap-lever/pull/16)

## 0.1.2
 * Fix exception when a candidate/opportunity does not have a resume [#14](https://github.com/singer-io/tap-lever/pull/14)

## 0.1.1
 * Remove pagination from Resume streams [#11](https://github.com/singer-io/tap-lever/pull/11)
