# hash_table.py

class Contact:
    """
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    """
    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    """
    Node class for separate chaining in the hash table.
    Attributes:
        key (str): The contact name, used as the key.
        value (Contact): The Contact object.
        next (Node | None): Pointer to next node in the chain.
    """
    def __init__(self, key: str, value: Contact):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    HashTable using separate chaining with linked lists of Node objects.
    Attributes:
        size (int): Fixed size of the underlying array.
        data (list[Node | None]): Array where each slot points to a chain (or None).
    Methods:
        hash_function(key): Map a string key to an index.
        insert(key, number): Insert or update a contact.
        search(key): Return the Contact with matching name, or None.
        print_table(): Print the table in the assignment's format.
    """
    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("HashTable size must be positive")
        self.size = size
        self.data = [None] * size

    def hash_function(self, key: str) -> int:
        total = 0
        for ch in key:
            total += ord(ch)
        return total % self.size

    def insert(self, key: str, number: str) -> None:
        """
        Insert a contact (key=name, number=phone). If the key already exists,
        update that contact's number.
        """
        index = self.hash_function(key)
        new_contact = Contact(key, number)

        head = self.data[index]
        if head is None:
            self.data[index] = Node(key, new_contact)
            return

        current = head
        while current:
            # Update if key already exists
            if current.key == key:
                current.value.number = number
                return
            # Move to next. If we're at end, append
            if current.next is None:
                break
            current = current.next

        # Append new node at end of chain
        current.next = Node(key, new_contact)

    def search(self, key: str) -> Contact | None:
        """
        Return the Contact with the given key, or None if not found.
        """
        index = self.hash_function(key)
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self) -> None:
        for i in range(self.size):
            print(f"Index {i}:", end=" ")
            current = self.data[i]
            if current is None:
                print("Empty")
            else:
                while current:
                    print(f"- {current.value}", end=" ")
                    current = current.next
                print()  # newline at end of chain line



if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()
    '''
    Expected shape (indices may differ):
    Index 0: Empty
    Index 1: Empty
    Index 2: Empty
    Index 3: Empty
    Index 4: Empty
    Index 5: Empty
    Index 6: Empty
    Index 7: Empty
    Index 8: Empty
    Index 9: Empty
    '''

    # Add some values
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")

    # Print the new table structure
    print("\nAfter inserting John and Rebecca:")
    table.print_table()
    '''
    Sample (indices may differ):
    Index 0: Empty
    Index 1: Empty
    Index 2: Empty
    Index 3: Empty
    Index 4: Empty
    Index 5: Empty
    Index 6: Empty
    Index 7: - Rebecca: 111-555-0002
    Index 8: Empty
    Index 9: - John: 909-876-1234
    '''

    # Search for a value
    contact = table.search("John")
    print("\nSearch result:", contact)  # e.g., John: 909-876-1234

    # Edge Case #1 - Potential hash collisions (depends on hash function)
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")  # May collide with Amy depending on index

    print("\nAfter inserting Amy and May (possible collision chain):")
    table.print_table()
    '''
    Example if they collide:
    Index 5: - Amy: 111-222-3333 - May: 222-333-1111
    '''

    # Edge Case #2 - Duplicate Keys (update number)
    table.insert("Rebecca", "999-444-9999")
    print("\nAfter updating Rebecca's number:")
    table.print_table()

    # Edge Case #3 - Searching for a non-existent key
    print("\nSearch missing key 'Chris':", table.search("Chris"))  # None


"""
---------------------------
Design Memo (≈ 230 words)
---------------------------

Why is a hash table the right structure for fast lookups?
A hash table offers average-case O(1) time for insert and search by computing
a hash of the key and jumping directly to its bucket index. For a contact list
indexed by unique names, this constant-time access pattern is ideal: rather
than scanning through every contact (like a list), we compute an index from
the name and inspect only a small chain.

How did you handle collisions?
This implementation uses separate chaining. Each array slot holds the head of
a singly linked list of Node objects. When two different names hash to the
same index, we append the new node to that chain. On inserts, if a node with
the same key already exists, we update the existing Contact’s number rather
than duplicating entries. This keeps chains short and preserves uniqueness.

When might an engineer choose a hash table over a list or tree?
Choose a hash table when the dominant operations are exact-key insert/find/
update and order does not matter—e.g., phone books keyed by name, caches,
symbol tables, or deduplicating sets. Compared to a Python list, a hash table
avoids O(n) scans for lookups. Compared to ordered trees, a hash table often
provides better constant factors and O(1) average behavior, though trees have
advantages when you need sorted iteration, predecessor/successor queries, or
range queries (operations that a hash table can’t do efficiently). Engineers
also consider load factor, memory overhead, and worst-case behavior; when
deterministic O(log n) bounds or ordering are required, trees can be preferable.
"""
