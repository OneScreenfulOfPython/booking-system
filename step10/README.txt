Add a user via an HTML form on the /users page.

This required adding a general-purpose execute function for SQL,
an add_user_to_database function which creates a user from a name
and (optional) email address, and trapping the /add-user URL.

Note the redirect once the form's complete: this is standard practice
as it avoids the possibility of backing into a POST-ed form. (These days,
most browsers avoid doing that anyway or warn you but the POST-then-301
dance is still considered good practice).

The effect here is that, once you've pressed "Add User", the screen
comes back to the users again with the new one added.