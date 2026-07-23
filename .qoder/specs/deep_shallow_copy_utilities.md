# Implementation Spec: Deep Copy and Shallow Copy Utilities

## Overview
Add deep copy and shallow copy utility classes to support both Java backend and JavaScript/React frontend. These utilities will provide reliable, easy-to-use copy functionality following existing project patterns.

---

## Implementation Files

### 1. Java Utility: `src/main/java/com/teacher/util/CopyUtil.java`

**Purpose**: Provide deep copy and shallow copy for Java objects

**Key Requirements**:
- File header comments: "始终生效" (line 1) and "自由万岁" (line 2) per project rules
- Package: `com.teacher.util` (new package to create)
- Class: `public final class CopyUtil` with private constructor
- Static utility methods following existing logger pattern from `TeacherServiceImpl.java:15`
- Use `java.util.logging.Logger` for error logging

**Method Signatures**:
```java
public static <T extends Serializable> T deepCopy(T object)
public static <T> T shallowCopy(T object)
public static <T extends Serializable> List<T> deepCopyList(List<T> list)
public static <T> List<T> shallowCopyList(List<T> list)
```

**Deep Copy Implementation**:
- **Strategy**: Java Object Serialization (ByteArrayOutputStream → ObjectOutputStream → ByteArrayInputStream → ObjectInputStream)
- **Process**:
  1. Null check → return null
  2. Immutable type check (String, Integer, etc.) → return same reference (optimization)
  3. Serialize object to byte array
  4. Deserialize from byte array to create independent copy
  5. Use try-with-resources for stream management
  6. Log errors with `logger.severe()` on failure
  7. Throw `IllegalArgumentException` if object not Serializable
  8. Throw `RuntimeException` wrapping IOException/ClassNotFoundException

- **Advantage**: Automatically handles nested objects and complex graphs
- **Limitation**: Requires objects to implement `Serializable` interface

**Shallow Copy Implementation**:
- **Strategy**: Reflection-based field copying
- **Process**:
  1. Null check → return null
  2. Get object class using `getClass()`
  3. Create new instance via default constructor using reflection
  4. Get all declared fields via `getDeclaredFields()`
  5. For each field: set accessible, copy value from source to target
  6. Log errors with `logger.severe()` on failure
  7. Throw `RuntimeException` wrapping reflection exceptions

- **Advantage**: Fast, works without Serializable
- **Limitation**: Requires accessible default constructor

**List Copy Helpers**:
- **Deep List**: Create new ArrayList, iterate and deepCopy each element
- **Shallow List**: Use ArrayList copy constructor `new ArrayList<>(sourceList)`

**Edge Cases**:
- Null input → return null
- Immutable objects (String, Integer, etc.) → return same instance for performance
- Circular references → handled by serialization mechanism
- Non-serializable deep copy → throw clear exception
- No default constructor shallow copy → throw clear exception

**Logging Pattern** (following `TeacherServiceImpl.java`):
- Method entry: `logger.fine("进入方法: deepCopy")`
- Errors: `logger.severe("深拷贝失败: " + e.getMessage())`
- Success: `logger.info("深拷贝完成: class=" + obj.getClass().getName())`

**Dependencies** (all JDK built-in):
```java
import java.io.*;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;
```

**JavaDoc Requirements**:
- Class-level: Purpose, usage examples, Serializable requirement note
- Method-level: Description, @param, @return, @throws, code examples
- Note thread safety (stateless utility, thread-safe)

**Must Support**: Deep copying `Teacher` entity (ensure Teacher implements Serializable)

---

### 2. Teacher Entity Update: `src/main/java/com/teacher/entity/Teacher.java`

**Purpose**: Make Teacher compatible with deep copy

**Change Required**:
```java
public class Teacher implements Serializable {
    private static final long serialVersionUID = 1L;
    // ... rest unchanged
}
```

**Rationale**: Teacher must implement Serializable for deep copy support

---

### 3. JavaScript Utility: `my-app/src/utils/copy.js`

**Purpose**: Provide deep copy and shallow copy for JavaScript objects

**Key Requirements**:
- ES6 module with named exports
- Follow logger.js pattern (ES6 class structure, default export for classes)
- No external dependencies (pure JavaScript)
- Handle circular references (critical for JavaScript)

**Exported Functions**:
```javascript
export function deepCopy(obj, cache = new WeakMap())
export function shallowCopy(obj)
```

**Deep Copy Implementation**:
- **Strategy**: Recursive traversal with WeakMap-based circular reference detection
- **Process**:
  1. **Primitive check**: Return primitives directly (number, string, boolean, null, undefined, symbol, bigint)
  2. **Cache check**: If `cache.has(obj)` → return `cache.get(obj)` (prevents infinite loop)
  3. **Special type handling**:
     - Date: `new Date(obj.getTime())`
     - RegExp: `new RegExp(obj.source, obj.flags)`
     - Map: Create new Map, recursively deep copy each key-value pair
     - Set: Create new Set, recursively deep copy each value
     - Function: Return original reference (functions not copied)
     - Typed Arrays (Int8Array, etc.): `new obj.constructor(obj)`
  4. **Array handling**:
     - Create new empty array `[]`
     - Add to cache IMMEDIATELY: `cache.set(obj, result)`
     - Recursively deepCopy each element
     - Return array
  5. **Plain object handling**:
     - Create new object with same prototype: `Object.create(Object.getPrototypeOf(obj))`
     - Add to cache IMMEDIATELY: `cache.set(obj, result)`
     - Recursively deepCopy each property (use `Object.keys` + `Object.getOwnPropertySymbols`)
     - Return object
  6. **Other types**: Return original reference (DOM nodes, class instances without special handling)

- **Circular Reference Solution**:
  - WeakMap cache: `Map<original_object, copied_object>`
  - CRITICAL: Add object to cache BEFORE recursing into its properties
  - When circular reference encountered, cache returns already-created copy
  - Example: `obj.self = obj` → cache ensures `copy.self === copy`

- **Advantage**: Handles any JavaScript type, prevents infinite loops
- **Limitation**: Functions and DOM nodes returned as references

**Shallow Copy Implementation**:
- **Strategy**: Object.assign + spread operator
- **Process**:
  1. Null/undefined check → return as-is
  2. Primitive check → return value
  3. Array check → use spread `[...arr]`
  4. Plain object check → use spread `{...obj}` or `Object.assign({}, obj)`
  5. Special types (Date, Map, Set) → create new instance with original data
  6. Other types → return original reference

- **Advantage**: Fast, simple, predictable
- **Limitation**: Nested objects/arrays share references

**Helper Functions** (not exported):
```javascript
function isPrimitive(value) {
  return value == null || (typeof value !== 'object' && typeof value !== 'function');
}

function isPlainObject(obj) {
  return Object.prototype.toString.call(obj) === '[object Object]';
}

function cloneSpecialType(obj) {
  // Handles Date, RegExp, Map, Set, typed arrays
  // Returns new instance or null if not special type
}
```

**Edge Cases**:
- Circular references → handled by WeakMap cache
- Date objects → preserve timestamp exactly
- RegExp → preserve pattern and flags (g, i, m, s, u, y)
- Map/Set → deep copy keys and values
- Sparse arrays `[1, , 3]` → preserve holes
- Null vs undefined → preserve distinction
- Symbol properties → copy using `Object.getOwnPropertySymbols()`
- Prototype chain → preserve using `Object.create(Object.getPrototypeOf(obj))`

**Optional Logger Integration** (following logger.js pattern):
```javascript
import Logger from './logger';
const logger = new Logger('CopyUtil');

// Use in error cases:
logger.error('Deep copy failed:', error);
logger.warn('Unexpected type encountered:', typeof obj);
```

**JSDoc Requirements**:
- File-level: Module description, version, author
- Function-level: Description, @param, @returns, @example with code
- Note: Circular reference handling, supported types

**Usage Examples** (for JSDoc):
```javascript
// Example 1: Deep copy with nested objects
const original = { user: { name: 'John', age: 30 } };
const copy = deepCopy(original);
copy.user.name = 'Jane';
console.log(original.user.name); // 'John' - unchanged

// Example 2: Circular reference
const obj = { name: 'Test' };
obj.self = obj;
const copy = deepCopy(obj);
console.log(copy.self === copy); // true

// Example 3: Shallow copy
const original = { items: [1, 2, 3] };
const copy = shallowCopy(original);
copy.items.push(4);
console.log(original.items); // [1, 2, 3, 4] - shared!
```

---

## Implementation Sequence

### Phase 1: Java Implementation
1. Create directory: `src/main/java/com/teacher/util/`
2. Create `CopyUtil.java` with headers ("始终生效" + "自由万岁")
3. Implement private constructor and logger instance
4. Implement `deepCopy()` with serialization approach
5. Implement `shallowCopy()` with reflection approach
6. Implement list helper methods
7. Add comprehensive JavaDoc
8. Update `Teacher.java` to implement Serializable

### Phase 2: JavaScript Implementation
1. Create `my-app/src/utils/copy.js`
2. Implement helper functions (isPrimitive, isPlainObject, cloneSpecialType)
3. Implement `deepCopy()` with WeakMap cache
4. Implement `shallowCopy()`
5. Add comprehensive JSDoc
6. Optional: Import and use Logger for error tracking

### Phase 3: Validation (if testing permitted)
1. Test Java deep copy with Teacher entity
2. Test Java shallow copy
3. Test JavaScript deep copy with circular references
4. Test JavaScript shallow copy
5. Verify logger integration

---

## Critical Files Summary

**Files to Create**:
1. `src/main/java/com/teacher/util/CopyUtil.java` - Java utility (250-300 lines)
2. `my-app/src/utils/copy.js` - JavaScript utility (180-220 lines)

**Files to Modify**:
1. `src/main/java/com/teacher/entity/Teacher.java` - Add `implements Serializable` (line 4)

**Reference Files** (no changes):
1. `src/main/java/com/teacher/service/impl/TeacherServiceImpl.java` - Logger pattern reference
2. `my-app/src/utils/logger.js` - JavaScript module pattern reference

---

## Success Criteria

**Functional**:
- ✅ Deep copy creates fully independent copies (no shared references except immutables)
- ✅ Shallow copy creates new container with shared internal references
- ✅ Null inputs handled gracefully
- ✅ Circular references don't cause infinite loops (JavaScript)
- ✅ Teacher entity deep copyable (Java)
- ✅ Error cases logged and throw appropriate exceptions

**Non-Functional**:
- ✅ Follow project code conventions (headers, logging, structure)
- ✅ Comprehensive documentation (JavaDoc/JSDoc)
- ✅ No external dependencies
- ✅ Code is maintainable and testable

---

## Key Design Decisions

**Java: Serialization over Clone**
- **Rationale**: Serialization automatically handles nested objects without manual recursion; more reliable for complex object graphs
- **Trade-off**: Requires Serializable interface, slower than manual copying
- **Mitigation**: Document requirement clearly, provide immutable type optimization

**JavaScript: WeakMap over Set**
- **Rationale**: WeakMap allows garbage collection of cached objects; keys are automatically cleaned up
- **Trade-off**: Slightly more complex than Set
- **Benefit**: Memory-safe, prevents memory leaks

**Static Methods over Instance Methods**
- **Rationale**: Utilities are stateless; static access is simpler (no instantiation needed)
- **Usage**: `CopyUtil.deepCopy(obj)` vs `new CopyUtil().deepCopy(obj)`

**No External Dependencies**
- **Rationale**: Project uses minimal dependencies; keep utilities lightweight
- **Benefit**: No version conflicts, easier maintenance, smaller bundle size

---

## Integration Points

**Java Potential Usage**:
- `TeacherServiceImpl.getAllTeachers()` - Return defensive copies
- Controller layer - Copy request objects before modification
- DAO layer - Create snapshots for audit trails

**JavaScript Potential Usage**:
- React state management - Copy state before setState
- Form handling - Copy form data before submission
- API response processing - Copy data before mutations

---

## Documentation & Comments

**Java Comments Style**:
- File header: "始终生效" (line 1) and "自由万岁" (line 2) - MANDATORY per project rules
- Chinese comments for method entry/success logs (follow TeacherServiceImpl pattern)
- English JavaDoc for API documentation
- Inline comments for complex logic (serialization process, reflection steps)

**JavaScript Comments Style**:
- No file header comments (not present in logger.js)
- English JSDoc for all exported functions
- Inline comments for circular reference logic
- Clear examples in JSDoc @example tags

---

## Testing Notes (for future)

**Java Test Cases**:
1. Deep copy Teacher → modify copy → verify original unchanged
2. Shallow copy Teacher → verify independent object
3. Deep copy List<Teacher> → verify list and elements independent
4. Shallow copy List<Teacher> → verify list independent but elements shared
5. Null handling all methods
6. Non-Serializable object → verify exception
7. Immutable optimization → verify String/Integer return same instance

**JavaScript Test Cases**:
1. Deep copy nested object → verify independence
2. Circular reference → verify no infinite loop, structure preserved
3. Date/RegExp/Map/Set → verify proper cloning
4. Shallow copy nested → verify shared references
5. Array with holes → verify holes preserved
6. Null/undefined handling
7. Primitives → verify returned as-is

天下为公
