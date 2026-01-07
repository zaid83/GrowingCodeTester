#!/usr/bin/env python3

"""
Growing Code Tester - Automated testing suite for Growing Code exercises
Inspired by libfttester principles

Usage: python3 growingcodetester.py [exercise_number|all]
"""

import sys
import os
import io
from typing import List
import importlib.util
import subprocess
import tempfile


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message


class GrowingCodeTester:
    def __init__(self):
        self.exercises = {
            0: ("ft_hello_garden", "ex0"),
            1: ("ft_plot_area", "ex1"),
            2: ("ft_harvest_total", "ex2"),
            3: ("ft_plant_age", "ex3"),
            4: ("ft_water_reminder", "ex4"),
            5: ("ft_count_harvest", "ex5"),
            6: ("ft_garden_summary", "ex6"),
            7: ("ft_seed_inventory", "ex7")
        }
        self.results = []
        self.compliance_results = []

    def print_header(self):
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("🌱 GROWING CODE TESTER 🌱")
        print("Automated Testing Suite for Growing Code Exercises")
        print("=" * 60)
        print(f"{Colors.END}")

    def capture_output(self, func, *args, **kwargs):
        """Capture stdout and return it along with any exception"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        try:
            result = func(*args, **kwargs)
            output = captured_output.getvalue()
            return output, None, result
        except Exception as e:
            output = captured_output.getvalue()
            return output, e, None
        finally:
            sys.stdout = old_stdout

    def simulate_input(self, inputs: List[str], func, *args, **kwargs):
        """Simulate user input for testing"""
        input_iter = iter(inputs)

        def mock_input(prompt=""):
            try:
                value = next(input_iter)
                print(f"{prompt}{value}")  # Show what was "typed"
                return value
            except StopIteration:
                raise EOFError("No more input available")

        # Temporarily replace input function
        if isinstance(__builtins__, dict):
            original_input = __builtins__['input']
            __builtins__['input'] = mock_input
        else:
            original_input = __builtins__.input
            __builtins__.input = mock_input

        try:
            return self.capture_output(func, *args, **kwargs)
        finally:
            # Restore original input
            if isinstance(__builtins__, dict):
                __builtins__['input'] = original_input
            else:
                __builtins__.input = original_input

    def check_compliance(self, exercise_name: str, directory: str):
        """Check code compliance with project requirements"""
        file_path = os.path.join(directory, f"{exercise_name}.py")

        if not os.path.exists(file_path):
            error_result = TestResult(
                f"{exercise_name}_compliance",
                False,
                "File not found"
            )
            return [error_result]

        compliance_tests = []

        # Check 0: File structure compliance
        expected_structure = {
            "ft_hello_garden": "ex0",
            "ft_plot_area": "ex1",
            "ft_harvest_total": "ex2",
            "ft_plant_age": "ex3",
            "ft_water_reminder": "ex4",
            "ft_count_harvest_iterative": "ex5",
            "ft_count_harvest_recursive": "ex5",
            "ft_garden_summary": "ex6",
            "ft_seed_inventory": "ex7"
        }

        if exercise_name in expected_structure:
            expected_dir = expected_structure[exercise_name]
            if directory == expected_dir:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_file_structure",
                    True,
                    "✓ Correct file structure"
                ))
            else:
                error_msg = (
                    f"❌ Should be in {expected_dir}/ directory, "
                    f"found in {directory}/"
                )
                error_result = TestResult(
                    f"{exercise_name}_file_structure",
                    False,
                    error_msg
                )
                compliance_tests.append(error_result)

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Check 1: Authorized functions only
            authorized_functions = {
                "ft_hello_garden": ["print"],
                "ft_plot_area": ["input", "int", "print"],
                "ft_harvest_total": ["input", "int", "print"],
                "ft_plant_age": ["input", "int", "print"],
                "ft_water_reminder": ["input", "int", "print"],
                "ft_count_harvest_iterative": ["input", "int", "print",
                                               "range"],
                "ft_count_harvest_recursive": ["input", "int", "print",
                                               "range"],
                "ft_garden_summary": ["input", "print"],
                "ft_seed_inventory": ["print", "capitalize"]
            }

            if exercise_name in authorized_functions:
                allowed = authorized_functions[exercise_name]
                # Simple check for unauthorized function calls
                import re
                # Find function calls (word followed by parentheses)
                pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
                function_calls = re.findall(pattern, content)
                # Filter out main function definition and built-in constructs
                unauthorized = []
                excluded_funcs = [
                    'if', 'for', 'while', 'def', 'class',
                    'try', 'except', 'with'
                ]
                for func in function_calls:
                    not_allowed = func not in allowed
                    not_main = func != exercise_name
                    not_excluded = func not in excluded_funcs
                    is_unauthorized = not_allowed and not_main and not_excluded
                    if is_unauthorized and func not in unauthorized:
                        unauthorized.append(func)

                if not unauthorized:
                    compliance_tests.append(TestResult(
                        f"{exercise_name}_authorized_functions",
                        True,
                        "✓ Uses only authorized functions"
                    ))
                else:
                    compliance_tests.append(TestResult(
                        f"{exercise_name}_authorized_functions",
                        False,
                        f"❌ Unauthorized functions: {', '.join(unauthorized)}"
                    ))

            # Check 2: No input validation
            has_validation = any([
                "< 0" in content,
                "> 0" in content,
                "<= 0" in content,
                ">= 0" in content,
                ("if" in content and ("negative" in content.lower() or
                                      "invalid" in content.lower()))
            ])

            if (has_validation and exercise_name != "ft_plant_age" and
                    exercise_name != "ft_water_reminder"):
                compliance_tests.append(TestResult(
                    f"{exercise_name}_no_validation",
                    False,
                    "❌ Should not handle input validation unless explicitly "
                    "mentioned"
                ))
            else:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_no_validation",
                    True,
                    "✓ No unnecessary input validation"
                ))

            # Check 3: Only requested function exists
            import ast
            tree = ast.parse(content)
            functions = [node.name for node in ast.walk(tree)
                         if isinstance(node, ast.FunctionDef)]

            if len(functions) == 1 and functions[0] == exercise_name:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_single_function",
                    True,
                    "✓ Contains only the requested function"
                ))
            else:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_single_function",
                    False,
                    f"❌ Should contain only {exercise_name}(), "
                    f"found: {functions}"
                ))

            # Check 4: Function name matches exactly
            if exercise_name in functions:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_correct_name",
                    True,
                    "✓ Function name matches exactly"
                ))
            else:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_correct_name",
                    False,
                    f"❌ Function {exercise_name} not found"
                ))

            # Check 5: Flake8 compliance using integrated flake8
            try:
                # Write content to temporary file for flake8 check
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py',
                                                 delete=False) as temp_file:
                    temp_file.write(content)
                    temp_file_path = temp_file.name

                # Run flake8 on the temporary file
                result = subprocess.run(
                    ['flake8', '--max-line-length=79', temp_file_path],
                    capture_output=True,
                    text=True
                )

                # Clean up temporary file
                os.unlink(temp_file_path)

                if result.returncode == 0:
                    compliance_tests.append(TestResult(
                        f"{exercise_name}_flake8",
                        True,
                        "✓ Flake8 compliant"
                    ))
                else:
                    # Parse flake8 output to get error messages
                    errors = (result.stdout.strip().split('\n')
                              if result.stdout.strip() else [])
                    error_summary = []
                    for error in errors[:3]:  # Show first 3 errors
                        if ':' in error:
                            parts = error.split(':')
                            if len(parts) >= 4:
                                line_num = parts[1]
                                error_code = parts[3].strip().split()[0]
                                error_summary.append(f"{error_code} "
                                                     f"(line {line_num})")

                    error_msg = '; '.join(error_summary)
                    if len(errors) > 3:
                        error_msg += '...'

                    compliance_tests.append(TestResult(
                        f"{exercise_name}_flake8",
                        False,
                        f"❌ Flake8 issues: {error_msg}"
                    ))

            except FileNotFoundError:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_flake8",
                    False,
                    "❌ Flake8 not installed (pip install flake8)"
                ))
            except Exception as e:
                compliance_tests.append(TestResult(
                    f"{exercise_name}_flake8",
                    False,
                    f"❌ Flake8 check failed: {str(e)}"
                ))

        except Exception as e:
            compliance_tests.append(TestResult(
                f"{exercise_name}_compliance",
                False,
                f"Error checking compliance: {e}"
            ))

        return compliance_tests

    def load_function(self, exercise_name: str, directory: str):
        """Load function from exercise file"""
        file_path = os.path.join(directory, f"{exercise_name}.py")

        if not os.path.exists(file_path):
            return None, f"File {file_path} not found"

        try:
            spec = importlib.util.spec_from_file_location(exercise_name,
                                                          file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, exercise_name):
                return getattr(module, exercise_name), None
            else:
                return None, f"Function {exercise_name} not found in " \
                             f"{file_path}"
        except Exception as e:
            return None, f"Error loading {file_path}: {str(e)}"

    def test_ex0_hello_garden(self):
        """Test Exercise 0: Hello Garden"""
        func, error = self.load_function("ft_hello_garden", "ex0")
        if error:
            return TestResult("ft_hello_garden", False, error)

        output, exception, _ = self.capture_output(func)

        if exception:
            return TestResult("ft_hello_garden", False,
                              f"Exception: {exception}")

        expected = "Hello, Garden community!"
        if expected in output:
            return TestResult("ft_hello_garden", True, "✓ Correct output")
        else:
            return TestResult("ft_hello_garden", False,
                              f"Expected '{expected}', got '{output.strip()}'")

    def test_ex1_plot_area(self):
        """Test Exercise 1: Plot Area"""
        func, error = self.load_function("ft_plot_area", "ex1")
        if error:
            return TestResult("ft_plot_area", False, error)

        # Test with inputs: length=5, width=3
        inputs = ["5", "3"]
        output, exception, _ = self.simulate_input(inputs, func)

        if exception:
            return TestResult("ft_plot_area", False,
                              f"Exception: {exception}")

        # Check if calculation is correct (5*3=15)
        if "15" in output:
            return TestResult("ft_plot_area", True, "✓ Correct calculation")
        else:
            return TestResult("ft_plot_area", False,
                              f"Expected area 15, got: {output}")

    def test_ex2_harvest_total(self):
        """Test Exercise 2: Harvest Total"""
        func, error = self.load_function("ft_harvest_total", "ex2")
        if error:
            return TestResult("ft_harvest_total", False, error)

        # Test with inputs: 5, 8, 3 (total should be 16)
        inputs = ["5", "8", "3"]
        output, exception, _ = self.simulate_input(inputs, func)

        if exception:
            return TestResult("ft_harvest_total", False,
                              f"Exception: {exception}")

        # Check if total calculation is correct (5+8+3=16)
        if "16" in output:
            return TestResult("ft_harvest_total", True,
                              "✓ Correct total calculation")
        else:
            return TestResult("ft_harvest_total", False,
                              f"Expected total 16, got: {output}")

    def test_ex3_plant_age(self):
        """Test Exercise 3: Plant Age Check"""
        func, error = self.load_function("ft_plant_age", "ex3")
        if error:
            return TestResult("ft_plant_age", False, error)

        # Test ready to harvest (>60 days)
        inputs = ["75"]
        output, exception, _ = self.simulate_input(inputs, func)

        if exception:
            return TestResult("ft_plant_age", False,
                              f"Exception: {exception}")

        if "ready to harvest" in output.lower():
            # Test boundary case (exactly 60 days - should NOT be ready)
            inputs = ["60"]
            output_boundary, exception_boundary, _ = self.simulate_input(
                inputs, func)

            if exception_boundary:
                return TestResult("ft_plant_age", False,
                                  f"Exception on boundary test: "
                                  f"{exception_boundary}")

            # Test not ready (<= 60 days)
            inputs = ["45"]
            output2, exception2, _ = self.simulate_input(inputs, func)

            if exception2:
                return TestResult("ft_plant_age", False,
                                  f"Exception on second test: {exception2}")

            boundary_not_ready = ("needs more time" in
                                  output_boundary.lower() or
                                  "not ready" in output_boundary.lower())
            young_not_ready = ("needs more time" in output2.lower() or
                               "not ready" in output2.lower())

            if boundary_not_ready and young_not_ready:
                return TestResult("ft_plant_age", True,
                                  "✓ Correct age checking logic (>60)")
            else:
                return TestResult("ft_plant_age", False,
                                  f"Wrong logic: 60 days -> "
                                  f"{output_boundary.strip()}, "
                                  f"45 days -> {output2.strip()}")
        else:
            return TestResult("ft_plant_age", False,
                              f"Wrong output for mature plant: {output}")

    def test_ex4_water_reminder(self):
        """Test Exercise 4: Water Reminder"""
        func, error = self.load_function("ft_water_reminder", "ex4")
        if error:
            return TestResult("ft_water_reminder", False, error)

        # Test needs watering (>2 days)
        inputs = ["4"]
        output, exception, _ = self.simulate_input(inputs, func)

        if exception:
            return TestResult("ft_water_reminder", False,
                              f"Exception: {exception}")

        if "Water the plants" in output:
            # Test boundary case (exactly 2 days - should be fine)
            inputs = ["2"]
            output_boundary, exception_boundary, _ = self.simulate_input(
                inputs, func)

            if exception_boundary:
                return TestResult("ft_water_reminder", False,
                                  f"Exception on boundary test: "
                                  f"{exception_boundary}")

            # Test plants are fine (<=2 days)
            inputs = ["1"]
            output2, exception2, _ = self.simulate_input(inputs, func)

            if exception2:
                return TestResult("ft_water_reminder", False,
                                  f"Exception on second test: {exception2}")

            boundary_fine = "Plants are fine" in output_boundary
            recent_fine = "Plants are fine" in output2

            if boundary_fine and recent_fine:
                return TestResult("ft_water_reminder", True,
                                  "✓ Correct watering logic (>2)")
            else:
                return TestResult("ft_water_reminder", False,
                                  f"Wrong logic: 2 days -> "
                                  f"{output_boundary.strip()}, "
                                  f"1 day -> {output2.strip()}")
        else:
            return TestResult("ft_water_reminder", False,
                              f"Wrong output for old watering: {output}")

    def test_ex5_count_harvest(self):
        """Test Exercise 5: Count to Harvest (both iterative and recursive)"""
        results = []

        # Test iterative version
        func_iter, error = self.load_function("ft_count_harvest_iterative",
                                              "ex5")
        if error:
            results.append(TestResult("ft_count_harvest_iterative", False,
                                      error))
        else:
            inputs = ["3"]
            output, exception, _ = self.simulate_input(inputs, func_iter)

            if exception:
                results.append(TestResult("ft_count_harvest_iterative", False,
                                          f"Exception: {exception}"))
            elif ("Day 1" in output and "Day 2" in output and
                  "Day 3" in output and "Harvest time" in output):
                results.append(TestResult("ft_count_harvest_iterative", True,
                                          "✓ Correct iterative counting"))
            else:
                results.append(TestResult("ft_count_harvest_iterative", False,
                                          f"Wrong counting output: {output}"))

        # Test recursive version
        func_rec, error = self.load_function("ft_count_harvest_recursive",
                                             "ex5")
        if error:
            results.append(TestResult("ft_count_harvest_recursive", False,
                                      error))
        else:
            inputs = ["3"]
            output, exception, _ = self.simulate_input(inputs, func_rec)

            if exception:
                results.append(TestResult("ft_count_harvest_recursive", False,
                                          f"Exception: {exception}"))
            elif ("Day 1" in output and "Day 2" in output and
                  "Day 3" in output and "Harvest time" in output):
                results.append(TestResult("ft_count_harvest_recursive", True,
                                          "✓ Correct recursive counting"))
            else:
                results.append(TestResult("ft_count_harvest_recursive", False,
                                          f"Wrong counting output: {output}"))

        return results

    def test_ex6_garden_summary(self):
        """Test Exercise 6: Garden Summary"""
        func, error = self.load_function("ft_garden_summary", "ex6")
        if error:
            return TestResult("ft_garden_summary", False, error)

        inputs = ["Community Garden", "25"]
        output, exception, _ = self.simulate_input(inputs, func)

        if exception:
            return TestResult("ft_garden_summary", False,
                              f"Exception: {exception}")

        checks = [
            "Community Garden" in output,
            "25" in output,
            "Growing well!" in output
        ]

        if all(checks):
            return TestResult("ft_garden_summary", True,
                              "✓ Correct summary format")
        else:
            return TestResult("ft_garden_summary", False,
                              f"Missing required elements in output: "
                              f"{output}")

    def test_ex7_seed_inventory(self):
        """Test Exercise 7: Seed Inventory with Type Annotations"""
        func, error = self.load_function("ft_seed_inventory", "ex7")
        if error:
            return TestResult("ft_seed_inventory", False, error)

        test_cases = [
            (("tomato", 15, "packets"), "packets available"),
            (("carrot", 8, "grams"), "grams total"),
            (("lettuce", 12, "area"), "square meters"),
            (("basil", 5, "unknown"), "Unknown unit type")
        ]

        for args, expected in test_cases:
            output, exception, _ = self.capture_output(func, *args)

            if exception:
                return TestResult("ft_seed_inventory", False,
                                  f"Exception with {args}: {exception}")

            if expected not in output:
                return TestResult("ft_seed_inventory", False,
                                  f"Expected '{expected}' for {args}, "
                                  f"got: {output}")

        return TestResult("ft_seed_inventory", True,
                          "✓ All unit types handled correctly")

    def run_test(self, exercise_num: int):
        """Run a specific test"""
        exercise_name, directory = self.exercises[exercise_num]

        print(f"\n{Colors.BLUE}Testing Exercise {exercise_num}: "
              f"{exercise_name}{Colors.END}")
        print("-" * 50)

        # Run compliance checks first
        if exercise_num == 5:  # Special case for ex5 with two functions
            compliance_iter = self.check_compliance(
                "ft_count_harvest_iterative", directory)
            compliance_rec = self.check_compliance(
                "ft_count_harvest_recursive", directory)
            self.compliance_results.extend(compliance_iter + compliance_rec)
        else:
            compliance = self.check_compliance(exercise_name, directory)
            self.compliance_results.extend(compliance)

        # Run functional tests
        if exercise_num == 0:
            result = self.test_ex0_hello_garden()
            self.results.append(result)
        elif exercise_num == 1:
            result = self.test_ex1_plot_area()
            self.results.append(result)
        elif exercise_num == 2:
            result = self.test_ex2_harvest_total()
            self.results.append(result)
        elif exercise_num == 3:
            result = self.test_ex3_plant_age()
            self.results.append(result)
        elif exercise_num == 4:
            result = self.test_ex4_water_reminder()
            self.results.append(result)
        elif exercise_num == 5:
            results = self.test_ex5_count_harvest()
            self.results.extend(results)
        elif exercise_num == 6:
            result = self.test_ex6_garden_summary()
            self.results.append(result)
        elif exercise_num == 7:
            result = self.test_ex7_seed_inventory()
            self.results.append(result)

    def print_result(self, result: TestResult):
        """Print a single test result"""
        status_color = Colors.GREEN if result.passed else Colors.RED
        status_symbol = "✅" if result.passed else "❌"

        print(f"{status_symbol} {Colors.BOLD}{result.name}{Colors.END}: "
              f"{status_color}{result.message}{Colors.END}")

    def print_summary(self):
        """Print final test summary"""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        compliance_passed = sum(1 for r in self.compliance_results
                                if r.passed)
        compliance_total = len(self.compliance_results)

        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"{Colors.END}")

        # Print compliance results
        if self.compliance_results:
            print(f"\n{Colors.MAGENTA}{Colors.BOLD}COMPLIANCE CHECKS:"
                  f"{Colors.END}")
            for result in self.compliance_results:
                self.print_result(result)

        # Print functional test results
        if self.results:
            print(f"\n{Colors.BLUE}{Colors.BOLD}FUNCTIONAL TESTS:"
                  f"{Colors.END}")
            for result in self.results:
                self.print_result(result)

        print(f"\n{Colors.BOLD}Compliance: {compliance_passed}/"
              f"{compliance_total} checks passed{Colors.END}")
        print(f"{Colors.BOLD}Functional: {passed}/{total} tests passed"
              f"{Colors.END}")

        if passed == total and compliance_passed == compliance_total:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests and compliance "
                  f"checks passed! 🎉{Colors.END}")
        elif compliance_passed < compliance_total:
            print(f"{Colors.YELLOW}⚠️  Fix compliance issues before "
                  f"submission!{Colors.END}")
        else:
            print(f"{Colors.YELLOW}💪 Keep working on the failing tests!"
                  f"{Colors.END}")


def main():
    tester = GrowingCodeTester()
    tester.print_header()

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "all":
            for i in range(8):
                tester.run_test(i)
        else:
            try:
                exercise_num = int(arg)
                if 0 <= exercise_num <= 7:
                    tester.run_test(exercise_num)
                else:
                    print(f"{Colors.RED}Error: Exercise number must be "
                          f"between 0 and 7{Colors.END}")
                    return
            except ValueError:
                print(f"{Colors.RED}Error: Invalid exercise number '{arg}'"
                      f"{Colors.END}")
                return
    else:
        print("Usage: python3 growingcodetester.py [0-7|all]")
        print("\nAvailable exercises:")
        for num, (name, _) in tester.exercises.items():
            print(f"  {num} - {name}")
        print("  all - Run all tests")
        return

    tester.print_summary()


if __name__ == "__main__":
    main()
