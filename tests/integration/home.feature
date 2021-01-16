Feature: Home API

  Scenario: It should return the root message
    Given the endpoint / is successfully requested
    Then the JSON response should be
      """
      {
        "message": "Hello from drivr's API."
      }
      """