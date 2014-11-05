django-ajaxtables
=================

Create simple ajax tables

## Adding sorable/hidable columns
- To make column sortable add `at-sort` class to the `<th>` element
- To make column hidable add `at-hide` class to the `<th>` element
- Set the `id` property of the `<th>` element.
    - The value of `id` will be passed as an argument to the `order_by()` function of the table's `queryset` on sorting
    - The `id` will be a key in the var `hidden` which is given to the template, so you can check whether the column is hidden or not