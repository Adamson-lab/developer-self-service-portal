# Identity and entitlements

`group-map.json` connects directory groups to the templates each team may request, and marks which groups may approve.

- Source of truth is Entra ID. A nightly job exports group membership to this file; manual edits are overwritten.
- Approver groups are separate from requester groups. A person in both can still not approve their own request (G-06).
- Changes are reviewed by Security because they change who can reach production.
