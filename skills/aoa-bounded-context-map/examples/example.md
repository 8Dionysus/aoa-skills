# Example

## Scenario

A product platform uses the word "account" to refer to customer identity, subscription billing, and workspace membership. Contributors keep placing changes in the wrong modules because those three concerns are mixed together in docs and code comments.

## Why this skill fits

- the main problem is semantic drift and overloaded terminology
- future changes need sharper boundaries before coding safely
- naming and interface clarity matter more here than immediate implementation

## Expected inputs

- the target subsystem where terminology is overloaded
- the current names and responsibilities attached to "account"
- known neighboring contexts such as identity, billing, and membership
- confusion points that have caused mis-scoped changes

## Expected outputs

- named contexts with a rough boundary map
- notes on what belongs inside each context
- interface or handoff notes between the contexts
- recommended vocabulary that reduces overload

## Boundary notes

- this example is about clarifying context boundaries, not redesigning the whole architecture
- it should reduce confusion first, then guide future code changes

## Verification notes

- confirm that the overloaded term was split into clearer context-specific language
- confirm that the handoff points between contexts are named
- confirm that a future contributor could place the next change more safely after reading the map
