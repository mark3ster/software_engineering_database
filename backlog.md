# Product Backlog

This document contains the system requirements identified from client feedback and testing.

## Requirement 1: Input Validation (Issue #23)

Description: The system must validate database keys and values before performing operations.

**Requirements:**
- Invalid keys or values must raise a `ValueError`.
- The `set()` and `delete()` methods must reject invalid input.
- The system must not silently reject invalid operations.
- Client applications must be able to detect errors through exceptions.


## Requirement 2: Documentation Consistency (Issue #24)

Description: The README must accurately reflect the database implementation.

**Requirements:**
- All documented methods must exist in the implementation.
- The methods `rebuild_index()` and `get_linear()` must be implemented if they are part of the specified API.
- The `delete()` method must follow the documented deletion behaviour.
- Documentation must be updated whenever the implementation changes.


## Requirement 3: Whitespace Preservation in Keys (Issue #25)

Description: The database must preserve the exact keys provided by users.

**Requirements:**
- Leading and trailing spaces must be preserved.
- Keys must not be automatically stripped or modified.
- `"  a"` and `"a"` must be treated as different keys.
- The `set()`, `get()` and `delete()` methods must handle whitespace consistently.


## Backlog Summary

 Issue  Requirement 

 #23  Input validation 
 #24  Documentation consistency
 #25  Whitespace preservation 