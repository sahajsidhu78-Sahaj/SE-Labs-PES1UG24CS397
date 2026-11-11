import re

_LINK_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)


def sender_domain(email):
    """Return the lower-cased domain of an email address, or "" if invalid."""
    if not isinstance(email, str):
        return ""
    local, at, domain = email.strip().rpartition("@")
    if not at or not local or not domain:
        return ""
    return domain.lower()


def first_link(text):
    """Return the first http(s) link in the text, or "" if there is none."""
    if not isinstance(text, str):
        return ""
    match = _LINK_PATTERN.search(text)
    return match.group(0) if match else ""


def shout_ratio(text):
    """Return the fraction of letters that are uppercase (0.0 if no letters)."""
    if not isinstance(text, str):
        return 0.0
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    upper = [c for c in letters if c.isupper()]
    return len(upper) / len(letters)


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    print("Sender Domain:", result)

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    print("First Link:", result)

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)


if __name__ == "__main__":
    main()