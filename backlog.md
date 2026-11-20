# Product Backlog

This document has the requirements of our key-value database. In phase 1 they came from the client feedback and the tests. For phase 2 we wrote them as user stories with acceptance criteria and we sorted them with MoSCoW.

## Phase 1 (done)

### Requirement 1: Input Validation (Issue #23)
Description: The system must validate database keys and values before doing anything.

Requirements:
* Invalid keys or values must raise a `ValueError`.
* The `set()` and `delete()` methods must reject invalid input.
* The system must not silently reject invalid operations.
* Client applications must be able to detect errors through exceptions.

### Requirement 2: Documentation Consistency (Issue #24)
Description: The README must match what the database really does.

Requirements:
* All documented methods must exist in the implementation.
* The methods `rebuild_index()` and `get_linear()` must be implemented if they are part of the API.
* The `delete()` method must follow the documented deletion behaviour.
* Documentation must be updated whenever the implementation changes.

### Requirement 3: Whitespace Preservation in Keys (Issue #25)
Description: The database must keep the exact keys that the user gives.

Requirements:
* Leading and trailing spaces must be preserved.
* Keys must not be stripped or changed.
* `" a"` and `"a"` must be different keys.
* The `set()`, `get()` and `delete()` methods must handle spaces in the same way.

| Issue | Requirement |
|-------|-------------|
| #23 | Input validation |
| #24 | Documentation consistency |
| #25 | Whitespace preservation |

## Phase 2 (segments)

The idea of phase 2 is that the file cannot grow forever. When a file gets too big we close it and start a new one (a "segment"). The rest of the database has to keep working like before.

### Must have

**US1. Maximum segment size in the README**
As a team member, I want the maximum size of a segment written in the README, so that it is a requirement and not something hidden in the code.
* The README says the unit (bytes) and the number.
* The README says what happens when a write does not fit.

**US2. Close the segment when it is full**
As a user, I want the database to start a new file when the current one is full, so that files do not grow forever.
* If the segment is at the maximum size, `set` and `delete` write in a new segment.
* A closed segment is never written again.
* Segments have names with a number, for example `data.1.db` and `data.2.db`.

**US3. `get` works in closed segments**
As a user, I want `get` to find values in old segments, so that I do not lose data when a segment closes.
* `self.index` saves the segment and the position of each key.
* `get` jumps to the position, it does not read the whole file.
* `get` of a key that does not exist still returns `None`.

**US4. Rebuild the index in order**
As a user, I want `rebuild_index()` to read the segments from the oldest to the newest, so that the last line of a key still wins after restarting.
* If a key is in segment 1 and again in segment 3, we get the value from segment 3.
* A tombstone in a newer segment hides the value in an older one.
* `test_value_with_comma_survives_restart` still passes.

**US5. `delete` and `list` with several segments**
As a user, I want `delete` and `list` to work with several segments, so that the API does not change.
* `list()` returns only the live keys of all the segments.
* `delete` of a key that does not exist writes nothing.

**US6. Tests from phase 1 stay green**
As a team, we want the 32 tests from E1 to keep passing, so that we do not break what already worked.
* The 32 tests pass and none of them is edited or removed.
* The GitHub Actions workflow is green before we merge.
* The tests for issues #23, #24 and #25 are included.

**US7. Tests for the segments**
As a team, we want tests (arrange, act, assert) for the segments, so that the new code is protected.
* There are tests for closing a segment, for `get` in a closed segment and for the ordered rebuild.
* Every bug we fix in this phase has a regression test. We write the test first and see it fail.

### Should have

**US8. Merge rule in the README**
As a team member, I want the merge rule written as a requirement, so that everybody knows what a merge keeps and what it drops.
* The README says that only the newest value of each key is kept.
* The README says when a tombstone can be dropped (only if no older segment has that key).

**US9. Merge closed segments**
As a user, I want to merge closed segments, so that the database uses less disk.
* After a merge, `get` and `list` give the same results as before.
* The segment that is being written is never merged.
* The merged data goes to a new segment and old files are not edited.

**US10. Segment size as a parameter**
As a developer, I want to choose the maximum size when I create the `Database`, so that the tests can use very small segments.
* `Database(path, max_segment_size=...)` works and the default value is in the README.
* A test can make several segments with only a few writes.

### Could have

**US11. Remove old segments after a merge**
* The new merged segment is fully written before the old ones are deleted.
* A temporary file left from a failed merge is ignored when the database starts.

**US12. Number of segments**
* There is a method or attribute that tells how many segments exist (useful for tests).

### Won't have (this phase)
* Hint files or snapshots of the index.
* Several processes writing at the same time.
* Crash recovery with checksums.
* Merging in the background.
* Command line.
