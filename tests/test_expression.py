import unittest

from spork.expression import Expression


class TestExpression(unittest.TestCase):
    def test_init(self):
        e1 = Expression("FromString")
        s1 = e1.to_string()

        expected_s1 = "FromString"

        # Creating an expression from another one should result in the same thing
        e2 = Expression(Expression("FromExpression"))
        s2 = "FromExpression"

        expected_s2 = "FromExpression"

        self.assertEqual(expected_s1, s1)
        self.assertEqual(expected_s2, s2)

    def test_negate(self):
        # Simple expression
        exp = ~Expression("True")
        exp_str = exp.to_string()
        expected_str = "not True"

        self.assertEqual(expected_str, exp_str)

        # Complex expression, outer negation
        outer_not = ~(Expression("AlsoTrue") & Expression("FurthermoreTrue"))
        outer_not_str = outer_not.to_string()
        expected_outer_not_str = "not (AlsoTrue and FurthermoreTrue)"

        self.assertEqual(expected_outer_not_str, outer_not_str)

        # Complex expression, nested negation
        inner_not = (Expression("AlsoTrue") & ~Expression("FurthermoreTrue"))
        inner_not_str = inner_not.to_string()
        expected_inner_not_str = "(AlsoTrue and not FurthermoreTrue)"

        self.assertEqual(expected_inner_not_str, inner_not_str)

    def test_eq_neq(self):
        lhs = Expression("lhs")
        rhs = Expression("rhs")

        # EQ
        result_eq1 = lhs.eq(rhs).to_string()
        expected_eq1 = "(lhs = rhs)"

        result_eq2 = rhs.eq(lhs).to_string()
        expected_eq2 = "(rhs = lhs)"

        self.assertEqual(result_eq1, expected_eq1)
        self.assertEqual(result_eq2, expected_eq2)

        # NEQ
        result_neq1 = lhs.neq(rhs).to_string()
        expected_neq1 = "(lhs <> rhs)"

        result_neq2 = rhs.neq(lhs).to_string()
        expected_neq2 = "(rhs <> lhs)"

        self.assertEqual(result_neq1, expected_neq1)
        self.assertEqual(result_neq2, expected_neq2)

    def test_binary_ops(self):
        lhs = Expression("lhs")
        rhs = Expression("rhs")

        # Logical Operators
        and_op = (lhs & rhs).to_string()
        expected_and_op = "(lhs and rhs)"

        or_op = (lhs | rhs).to_string()
        expected_or_op = "(lhs or rhs)"

        # Comparison Operators
        lt = (lhs < rhs).to_string()
        expected_lt = "(lhs < rhs)"

        leq = (lhs <= rhs).to_string()
        expected_leq = "(lhs <= rhs)"

        gt = (lhs > rhs).to_string()
        expected_gt = "(lhs > rhs)"

        geq = (lhs >= rhs).to_string()
        expected_geq = "(lhs >= rhs)"

        eq = lhs.eq(rhs).to_string()
        expected_eq = "(lhs = rhs)"

        neq = lhs.neq(rhs).to_string()
        expected_neq = "(lhs <> rhs)"

        # Arithmetic Operators
        add = (lhs + rhs).to_string()
        expected_add = "(lhs + rhs)"

        sub = (lhs - rhs).to_string()
        expected_sub = "(lhs - rhs)"

        mul = (lhs * rhs).to_string()
        expected_mul = "(lhs * rhs)"

        div = (lhs / rhs).to_string()
        expected_div = "(lhs / rhs)"

        mod = (lhs % rhs).to_string()
        expected_mod = "(lhs % rhs)"

        # Assertions for all operations
        self.assertEqual(expected_and_op, and_op)
        self.assertEqual(expected_or_op, or_op)
        self.assertEqual(expected_lt, lt)
        self.assertEqual(expected_leq, leq)
        self.assertEqual(expected_gt, gt)
        self.assertEqual(expected_geq, geq)
        self.assertEqual(expected_eq, eq)
        self.assertEqual(expected_neq, neq)
        self.assertEqual(expected_add, add)
        self.assertEqual(expected_sub, sub)
        self.assertEqual(expected_mul, mul)
        self.assertEqual(expected_div, div)
        self.assertEqual(expected_mod, mod)

    def test_alias(self):
        # Simple alias
        exp = Expression("BaseExpression").alias("Aliased").to_string()
        expected_exp_str = "BaseExpression as Aliased"
        self.assertEqual(expected_exp_str, exp)

        # Outer alias on a complex expression
        outer_alias = (Expression("A") & Expression("B")).alias("OuterAlias").to_string()
        expected_outer_alias = "(A and B) as OuterAlias"
        self.assertEqual(expected_outer_alias, outer_alias)

        # Nested alias
        nested_alias = (Expression("X").alias("InnerAlias") & Expression("Y")).to_string()
        expected_nested_alias = "(X and Y)"
        self.assertEqual(expected_nested_alias, nested_alias)

    def test_cast(self):
        # Simple cast
        exp = Expression("BaseExpression").cast("decimal").to_string()
        expected_exp_str = "BaseExpression::decimal"
        self.assertEqual(expected_exp_str, exp)

        # Outer cast on a complex expression
        outer_cast = (Expression("A") & Expression("B")).cast("text").to_string()
        expected_outer_cast = "(A and B)::text"
        self.assertEqual(expected_outer_cast, outer_cast)

        # Nested cast
        nested_cast = (Expression("X").cast("int") & Expression("Y")).to_string()
        expected_nested_cast = "(X::int and Y)"
        self.assertEqual(expected_nested_cast, nested_cast)

    def test_null_check(self):
        exp_is = Expression("Nullables").is_null().to_string()
        exp_is_not = Expression("Nullables").is_not_null().to_string()

        self.assertEqual("Nullables is null", exp_is)
        self.assertEqual("Nullables is not null", exp_is_not)


if __name__ == "__main__":
    unittest.main()
