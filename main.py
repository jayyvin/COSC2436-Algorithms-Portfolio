import time

# ============================================================
# PART 1: Three Classic Hash Table (dict) Use Cases
# ============================================================

# ---- Use Case 1: Lookup Tool (Contact Book) ----

def add_contact(contact_book, name, number):
    """
    Add a name/number pair to the contact_book dictionary.
    contact_book: dict mapping name -> phone number
    """
    contact_book[name] = number


def lookup_contact(contact_book, name):
    """
    Look up a name in the contact_book.
    Return the phone number if found, or the string "Not found" if missing.
    """
    return contact_book.get(name, "Not found")


# ---- Use Case 2: Duplicate-Catcher (Voter Check) ----

def check_voter(voted_dict, name):
    """
    Check whether 'name' has already voted.
    voted_dict: dict mapping name -> True (if they voted)

    Returns:
        "Allowed to vote" or "Already voted!"
    """
    if name in voted_dict:
        return "Already voted!"
    else:
        voted_dict[name] = True
        return "Allowed to vote"


# ---- Use Case 3: Cache Simulator (Web Page Cache) ----

def simulate_server_call(url):
    """
    Pretend this is an expensive network/server call.
    This helper is already implemented for you - do not modify.
    """
    time.sleep(0.01)
    return "Contents of " + url


def get_page(cache, url):
    """
    Return the page contents for 'url', using 'cache' (a dict)
    to avoid repeating expensive simulate_server_call() calls.
    """
    if url in cache:
        print("HIT:", url)
        return cache[url]
    else:
        print("MISS:", url)
        result = simulate_server_call(url)
        cache[url] = result
        return result


# ============================================================
# PART 2: Build Your Own Mini Hash Table
# ============================================================

def simple_hash(key, num_slots):
    """
    A simple hash function: sum the character codes of key,
    then mod by num_slots.
    """
    total = 0
    for char in key:
        total += ord(char)
    return total % num_slots


class MiniHashTable:
    """
    A simplified hash table built on a plain Python list.
    Collisions are handled with chaining.
    """

    def __init__(self, num_slots):
        self.num_slots = num_slots
        self.slots = [[] for _ in range(num_slots)]
        self.num_items = 0

    def insert(self, key, value):
        index = simple_hash(key, self.num_slots)
        chain = self.slots[index]

        for i in range(len(chain)):
            existing_key, existing_value = chain[i]
            if existing_key == key:
                chain[i] = (key, value)
                return

        chain.append((key, value))
        self.num_items += 1

    def get(self, key):
        index = simple_hash(key, self.num_slots)
        chain = self.slots[index]

        for existing_key, existing_value in chain:
            if existing_key == key:
                return existing_value

        return None

    def load_factor(self):
        return self.num_items / self.num_slots


# ============================================================
# PART 3: Load Factor & Hash Quality Investigation
# ============================================================

def bad_hash(key, num_slots):
    """
    A deliberately weak hash function.
    """
    return len(key) % num_slots


def investigate_hash_quality(hash_func, keys, num_slots):
    """
    Return:
        (total_collisions, longest_chain_length)
    """
    chains = [[] for _ in range(num_slots)]
    total_collisions = 0

    for key in keys:
        index = hash_func(key, num_slots)

        if len(chains[index]) >= 1:
            total_collisions += 1

        chains[index].append(key)

    longest_chain_length = 0
    for chain in chains:
        if len(chain) > longest_chain_length:
            longest_chain_length = len(chain)

    return total_collisions, longest_chain_length


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # ---- Part 1 Demo: Contact Book ----
    contact_book = {}
    add_contact(contact_book, "Maggie", "555-1234")
    add_contact(contact_book, "Sam", "555-5678")

    print(lookup_contact(contact_book, "Maggie"))
    print(lookup_contact(contact_book, "NotInBook"))

    # ---- Part 1 Demo: Voter Check ----
    voted_dict = {}
    print(check_voter(voted_dict, "Tom"))
    print(check_voter(voted_dict, "Tom"))
    print(check_voter(voted_dict, "Lisa"))

    # ---- Part 1 Demo: Cache Simulator ----
    page_cache = {}

    urls_to_fetch = [
        "http://site.test/home",
        "http://site.test/about",
        "http://site.test/home",
        "http://site.test/contact",
        "http://site.test/home",
    ]

    for url in urls_to_fetch:
        page = get_page(page_cache, url)
        print(page)

    # ---- Part 2 Demo: Mini Hash Table ----
    mini_table = MiniHashTable(5)

    mini_table.insert("apple", 10)
    mini_table.insert("avocado", 20)
    mini_table.insert("banana", 30)

    print(mini_table.get("apple"))
    print(mini_table.get("avocado"))
    print(mini_table.get("missing_key"))
    print(mini_table.load_factor())

    # ---- Part 3 Demo: Hash Quality Investigation ----
    sample_keys = [
        "Maggie",
        "Tom",
        "Lisa",
        "Sam",
        "Ella",
        "Noah",
        "Ava",
        "Liam",
        "Mia",
        "Ethan",
        "Grace",
        "Oliver",
    ]

    num_slots = 8

    good_collisions, good_longest = investigate_hash_quality(
        simple_hash, sample_keys, num_slots
    )
    print(good_collisions)
    print(good_longest)

    bad_collisions, bad_longest = investigate_hash_quality(
        bad_hash, sample_keys, num_slots
    )
    print(bad_collisions)
    print(bad_longest)