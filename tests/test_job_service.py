import unittest
from unittest.mock import MagicMock

from src.discovery_api.services.JobService import JobService
from src.discovery_api.services.BaseQuery import BaseQuery


class TestJobService(unittest.TestCase):
    """Unit tests for the JobService class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_base_query = MagicMock(spec=BaseQuery)
        self.job_service = JobService(self.mock_base_query)
        
        # Mock operation and job objects
        self.mock_op = MagicMock()
        self.mock_job = MagicMock()
        
        # Set up return values for create_job_query method
        self.mock_base_query.create_job_query.return_value = (self.mock_op, self.mock_job)
        
        # Common test data
        self.test_job_id = 456
        self.test_unique_id = "model.test_project.test_model"
        
        # Standard mock response
        self.mock_job_response = {
            "data": {
                "job": {
                    "id": self.test_job_id,
                    "run_id": 123,
                    "models": [
                        {
                            "name": "test_model",
                            "unique_id": self.test_unique_id,
                            "description": "Test model description",
                            "tags": ["test", "model"],
                            "resource_type": "model",
                            "database": "test_db",
                            "schema": "test_schema",
                            "alias": "test_model_alias",
                            "run_id": 123,
                            "job_id": self.test_job_id,
                            "status": "success"
                        }
                    ],
                    "tests": [
                        {
                            "name": "test_assertion",
                            "unique_id": "test.test_project.test_assertion",
                            "description": "Test assertion description",
                            "tags": ["test"],
                            "resource_type": "test",
                            "run_id": 123,
                            "job_id": self.test_job_id,
                            "status": "success"
                        }
                    ]
                }
            }
        }

    def test_convert_keys_to_snake_case(self):
        """Test _convert_keys_to_snake_case method."""
        # Test with camelCase dict
        camel_case_dict = {
            "userId": 1,
            "firstName": "John",
            "lastName": "Doe",
            "nestedObject": {
                "phoneNumber": "123-456-7890",
                "emailAddress": "john.doe@example.com"
            },
            "arrayItems": [
                {"itemId": 1, "itemName": "Item 1"},
                {"itemId": 2, "itemName": "Item 2"}
            ]
        }
        
        expected_result = {
            "user_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "nested_object": {
                "phone_number": "123-456-7890",
                "email_address": "john.doe@example.com"
            },
            "array_items": [
                {"item_id": 1, "item_name": "Item 1"},
                {"item_id": 2, "item_name": "Item 2"}
            ]
        }
        
        result = self.job_service._convert_keys_to_snake_case(camel_case_dict)
        self.assertEqual(result, expected_result)
        
        # Test with list
        list_input = [
            {"userId": 1, "userName": "user1"},
            {"userId": 2, "userName": "user2"}
        ]
        
        expected_list_result = [
            {"user_id": 1, "user_name": "user1"},
            {"user_id": 2, "user_name": "user2"}
        ]
        
        result = self.job_service._convert_keys_to_snake_case(list_input)
        self.assertEqual(result, expected_list_result)
        
        # Test with non-dict, non-list value
        result = self.job_service._convert_keys_to_snake_case("simple string")
        self.assertEqual(result, "simple string")
        
        result = self.job_service._convert_keys_to_snake_case(123)
        self.assertEqual(result, 123)

    def test_add_job_fields(self):
        """Test _add_job_fields method."""
        mock_job = MagicMock()
        self.job_service._add_job_fields(mock_job)
        
        # Verify the correct fields are added
        mock_job.id.assert_called_once()
        mock_job.run_id.assert_called_once()

    def test_add_model_fields(self):
        """Test _add_model_fields method with default settings (all fields)."""
        mock_model = MagicMock()
        self.job_service._add_model_fields(mock_model)
        
        # Verify basic fields are added
        mock_model.name.assert_called_once()
        mock_model.unique_id.assert_called_once()
        mock_model.description.assert_called_once()
        mock_model.tags.assert_called_once()
        mock_model.resource_type.assert_called_once()
        
        # Verify database fields are added
        mock_model.database.assert_called_once()
        mock_model.schema.assert_called_once()
        mock_model.alias.assert_called_once()
        
        # Verify run metadata fields are added
        mock_model.run_id.assert_called_once()
        mock_model.job_id.assert_called_once()
        
        # Verify execution timing fields are added
        mock_model.execution_time.assert_called_once()
        mock_model.run_elapsed_time.assert_called_once()
        
        # Verify status fields are added
        mock_model.status.assert_called_once()
        mock_model.error.assert_called_once()
        
        # Verify code fields are added
        mock_model.raw_sql.assert_called_once()
        mock_model.compiled_sql.assert_called_once()
    
    def test_add_model_fields_with_selective_fields(self):
        """Test _add_model_fields method with selective field groups."""
        # Test with only database fields
        mock_model = MagicMock()
        self.job_service._add_model_fields(mock_model, include_database=True)
        
        # Basic fields should always be included
        mock_model.name.assert_called_once()
        mock_model.unique_id.assert_called_once()
        mock_model.resource_type.assert_called_once()
        
        # Database fields should be included
        mock_model.database.assert_called_once()
        mock_model.schema.assert_called_once()
        
        # Run metadata fields should not be included
        mock_model.run_id.assert_not_called()
        mock_model.job_id.assert_not_called()
        
        # Code fields should not be included
        mock_model.raw_sql.assert_not_called()
        mock_model.compiled_sql.assert_not_called()
        
        # Test with only code fields
        mock_model = MagicMock()
        self.job_service._add_model_fields(mock_model, include_code=True)
        
        # Basic fields should always be included
        mock_model.name.assert_called_once()
        mock_model.unique_id.assert_called_once()
        
        # Database fields should not be included
        mock_model.database.assert_not_called()
        mock_model.schema.assert_not_called()
        
        # Code fields should be included
        mock_model.raw_sql.assert_called_once()
        mock_model.compiled_sql.assert_called_once()
        
        # Test with include_all=True
        mock_model = MagicMock()
        self.job_service._add_model_fields(mock_model, include_all=True)
        
        # All field groups should be included
        mock_model.name.assert_called_once()
        mock_model.database.assert_called_once()
        mock_model.run_id.assert_called_once()
        mock_model.execution_time.assert_called_once()
        mock_model.status.assert_called_once()
        mock_model.raw_sql.assert_called_once()

    def test_add_test_fields(self):
        """Test _add_test_fields method with default settings (all fields)."""
        mock_test = MagicMock()
        self.job_service._add_test_fields(mock_test)
        
        # Verify basic fields are added
        mock_test.name.assert_called_once()
        mock_test.unique_id.assert_called_once()
        mock_test.description.assert_called_once()
        mock_test.tags.assert_called_once()
        mock_test.resource_type.assert_called_once()
        
        # Verify run metadata fields are added
        mock_test.run_id.assert_called_once()
        mock_test.job_id.assert_called_once()
        
        # Verify execution timing fields are added
        mock_test.execution_time.assert_called_once()
        mock_test.run_elapsed_time.assert_called_once()
        
        # Verify status fields are added
        mock_test.status.assert_called_once()
        mock_test.error.assert_called_once()
        mock_test.state.assert_called_once()
        mock_test.fail.assert_called_once()
        
        # Verify code fields are added
        mock_test.raw_sql.assert_called_once()
        mock_test.compiled_sql.assert_called_once()
    
    def test_add_test_fields_with_selective_fields(self):
        """Test _add_test_fields method with selective field groups."""
        # Test with only status fields
        mock_test = MagicMock()
        self.job_service._add_test_fields(mock_test, include_status=True)
        
        # Basic fields should always be included
        mock_test.name.assert_called_once()
        mock_test.unique_id.assert_called_once()
        mock_test.resource_type.assert_called_once()
        
        # Status fields should be included
        mock_test.status.assert_called_once()
        mock_test.error.assert_called_once()
        mock_test.fail.assert_called_once()
        
        # Run metadata fields should not be included
        mock_test.run_id.assert_not_called()
        mock_test.job_id.assert_not_called()
        
        # Code fields should not be included
        mock_test.raw_sql.assert_not_called()
        mock_test.compiled_sql.assert_not_called()
        
        # Test with only timing fields
        mock_test = MagicMock()
        self.job_service._add_test_fields(mock_test, include_timing=True)
        
        # Basic fields should always be included
        mock_test.name.assert_called_once()
        mock_test.unique_id.assert_called_once()
        
        # Timing fields should be included
        mock_test.execution_time.assert_called_once()
        mock_test.run_elapsed_time.assert_called_once()
        
        # Status fields should not be included
        mock_test.status.assert_not_called()
        mock_test.error.assert_not_called()
        
        # Test with include_all=True
        mock_test = MagicMock()
        self.job_service._add_test_fields(mock_test, include_all=True)
        
        # All field groups should be included
        mock_test.name.assert_called_once()
        mock_test.run_id.assert_called_once()
        mock_test.execution_time.assert_called_once()
        mock_test.status.assert_called_once()
        mock_test.raw_sql.assert_called_once()

    def test_get_job_metadata(self):
        """Test get_job_metadata method."""
        # Configure mock response
        self.mock_base_query.execute.return_value = {
            "data": {
                "job": {
                    "id": self.test_job_id,
                    "runId": 123
                }
            }
        }
        
        # Call the method
        result = self.job_service.get_job_metadata(self.test_job_id)
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_base_query.execute.assert_called_once_with(self.mock_op)
        
        # Verify result
        self.assertEqual(result["id"], self.test_job_id)
        self.assertEqual(result["run_id"], 123)  # Snake case conversion

    def test_get_job_metadata_with_kwargs(self):
        """Test get_job_metadata with additional keyword arguments."""
        # Call the method with additional keyword arguments
        self.job_service.get_job_metadata(self.test_job_id, return_query=True)
        
        # Verify the keyword arguments are passed to execute
        self.mock_base_query.execute.assert_called_once_with(self.mock_op, return_query=True)

    def test_get_job_models(self):
        """Test get_job_models method."""
        # Configure mock response
        self.mock_base_query.execute.return_value = self.mock_job_response
        
        # Call the method
        result = self.job_service.get_job_models(self.test_job_id)
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.models.assert_called_once()
        self.mock_base_query.execute.assert_called_once_with(self.mock_op)
        
        # Verify result
        self.assertEqual(result["id"], self.test_job_id)
        self.assertEqual(len(result["models"]), 1)
        self.assertEqual(result["models"][0]["unique_id"], self.test_unique_id)
    
    def test_get_job_models_with_field_selection(self):
        """Test get_job_models method with field selection options."""
        # Configure mock response
        self.mock_base_query.execute.return_value = self.mock_job_response
        
        # Reset mock to clear previous calls
        self.mock_base_query.reset_mock()
        self.mock_job.reset_mock()
        
        # Call the method with field selection options
        result = self.job_service.get_job_models(
            self.test_job_id, 
            include_database=True, 
            include_code=True,
            return_query=True
        )
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.models.assert_called_once()
        
        # Verify execute was called with return_query=True
        self.mock_base_query.execute.assert_called_once_with(self.mock_op, return_query=True)

    def test_get_job_tests(self):
        """Test get_job_tests method."""
        # Configure mock response
        self.mock_base_query.execute.return_value = self.mock_job_response
        
        # Call the method
        result = self.job_service.get_job_tests(self.test_job_id)
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.tests.assert_called_once()
        self.mock_base_query.execute.assert_called_once_with(self.mock_op)
        
        # Verify result
        self.assertEqual(result["id"], self.test_job_id)
        self.assertEqual(len(result["tests"]), 1)
        self.assertEqual(result["tests"][0]["unique_id"], "test.test_project.test_assertion")
    
    def test_get_job_tests_with_field_selection(self):
        """Test get_job_tests method with field selection options."""
        # Configure mock response
        self.mock_base_query.execute.return_value = self.mock_job_response
        
        # Reset mock to clear previous calls
        self.mock_base_query.reset_mock()
        self.mock_job.reset_mock()
        
        # Call the method with field selection options
        result = self.job_service.get_job_tests(
            self.test_job_id, 
            include_status=True, 
            include_timing=True,
            return_query=True
        )
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.tests.assert_called_once()
        
        # Verify execute was called with return_query=True
        self.mock_base_query.execute.assert_called_once_with(self.mock_op, return_query=True)

    def test_get_job_model_by_unique_id(self):
        """Test get_job_model_by_unique_id method."""
        # Configure mock response
        self.mock_base_query.execute.return_value = {
            "data": {
                "job": {
                    "model": {
                        "name": "test_model",
                        "unique_id": self.test_unique_id,
                        "description": "Test model description"
                    }
                }
            }
        }
        
        # Call the method
        result = self.job_service.get_job_model_by_unique_id(self.test_job_id, self.test_unique_id)
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.model.assert_called_once_with(unique_id=self.test_unique_id)
        self.mock_base_query.execute.assert_called_once_with(self.mock_op)
        
        # Verify result
        self.assertEqual(result["name"], "test_model")
        self.assertEqual(result["unique_id"], self.test_unique_id)

    def test_get_job_model_by_unique_id_not_found(self):
        """Test get_job_model_by_unique_id when model is not found."""
        # Configure mock response for model not found
        self.mock_base_query.execute.return_value = {
            "data": {
                "job": {
                    "model": None
                }
            }
        }
        
        # Call the method
        result = self.job_service.get_job_model_by_unique_id(self.test_job_id, self.test_unique_id)
        
        # Verify result is None
        self.assertIsNone(result)

    def test_get_job_test_by_unique_id(self):
        """Test get_job_test_by_unique_id method."""
        test_unique_id = "test.test_project.test_assertion"
        
        # Configure mock response
        self.mock_base_query.execute.return_value = {
            "data": {
                "job": {
                    "test": {
                        "name": "test_assertion",
                        "unique_id": test_unique_id,
                        "description": "Test assertion description"
                    }
                }
            }
        }
        
        # Call the method
        result = self.job_service.get_job_test_by_unique_id(self.test_job_id, test_unique_id)
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.test.assert_called_once_with(unique_id=test_unique_id)
        self.mock_base_query.execute.assert_called_once_with(self.mock_op)
        
        # Verify result
        self.assertEqual(result["name"], "test_assertion")
        self.assertEqual(result["unique_id"], test_unique_id)

    def test_get_job_test_by_unique_id_not_found(self):
        """Test get_job_test_by_unique_id when test is not found."""
        test_unique_id = "test.test_project.nonexistent_test"
        
        # Configure mock response for test not found
        self.mock_base_query.execute.return_value = {
            "data": {
                "job": {
                    "test": None
                }
            }
        }
        
        # Call the method
        result = self.job_service.get_job_test_by_unique_id(self.test_job_id, test_unique_id)
        
        # Verify result is None
        self.assertIsNone(result)

    def test_get_job_with_models_and_tests(self):
        """Test get_job_with_models_and_tests method."""
        # Configure mock response
        self.mock_base_query.execute.return_value = self.mock_job_response
        
        # Call the method
        result = self.job_service.get_job_with_models_and_tests(self.test_job_id)
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.models.assert_called_once()
        self.mock_job.tests.assert_called_once()
        self.mock_base_query.execute.assert_called_once_with(self.mock_op)
        
        # Verify result
        self.assertEqual(result["id"], self.test_job_id)
        self.assertEqual(len(result["models"]), 1)
        self.assertEqual(result["models"][0]["unique_id"], self.test_unique_id)
        self.assertEqual(len(result["tests"]), 1)
        self.assertEqual(result["tests"][0]["unique_id"], "test.test_project.test_assertion")
    
    def test_get_job_with_models_and_tests_with_field_selection(self):
        """Test get_job_with_models_and_tests method with field selection options."""
        # Configure mock response
        self.mock_base_query.execute.return_value = self.mock_job_response
        
        # Reset mock to clear previous calls
        self.mock_base_query.reset_mock()
        self.mock_job.reset_mock()
        
        # Call the method with field selection options
        result = self.job_service.get_job_with_models_and_tests(
            self.test_job_id, 
            include_all=True,
            return_query=True
        )
        
        # Verify method calls
        self.mock_base_query.create_job_query.assert_called_once_with(self.test_job_id)
        self.mock_job.models.assert_called_once()
        self.mock_job.tests.assert_called_once()
        
        # Verify execute was called with return_query=True
        self.mock_base_query.execute.assert_called_once_with(self.mock_op, return_query=True)


if __name__ == '__main__':
    unittest.main()
