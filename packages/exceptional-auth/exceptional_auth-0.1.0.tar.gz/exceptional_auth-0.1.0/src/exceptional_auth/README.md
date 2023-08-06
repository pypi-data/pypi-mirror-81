# exceptional_auth

The purpose of this package is to provide a more flexible/powerful replacement for Django's `login_required` and `permission_required` decorators (and provide some entirely new related functionality).

The idea is to create a standard set of exceptions which any code can raise (even reusable apps distributed on pypi), and leave the handling of these exceptions up to the site developer (via custom middleware).

We provide `exceptional_auth.BaseMiddleware`, a Middleware base class which makes it easier to handle our exceptions. Site developers should write a custom middleware extending this class, and add to `MIDDLEWARE` setting.