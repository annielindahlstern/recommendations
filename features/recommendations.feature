Feature: The recommendation service back-end
    As a eCommerce web site Owner
    I need a RESTful catalog service
    So that I can keep track of all my recommendations

Background:
    Given the following recommendations
        | name   | original_product_id | recommendation_product_id | recommendation_product_name  | reason     | activated |
        | desk   | 1                   | 5                         | chair                        | CROSS_SELL | True      |
        | mouse  | 2                   | 6                         | keyboard                     | UP_SELL    | True      |
        | jelly  | 3                   | 7                         | beans                        | OTHER      | False     |
        | tea    | 4                   | 8                         | mug                          | ACCESSORY  | True      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "name" to "couch"
    And I set the "original_product_id" to "9"
    And I set the "product_name" to "tv"
    And I set the "product_id" to "10"
    And I select "UpSell" in the "Reason" dropdown
    And I select "True" in the "Activated" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "name" field should be empty
    And the "original_product_id" field should be empty
    And the "product_name" field should be empty
    And the "product_id" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "couch" in the "name" field
    And I should see "9" in the "original_product_id" field
    And I should see "tv" in the "product_name" field
    And I should see "10" in the "product_id" field
    And I should see "UpSell" in the "Reason" dropdown
    And I should see "True" in the "Activated" dropdown


Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "desk" in the results
    And I should see "mouse" in the results
    And I should see "jelly" in the results
    And I should see "tea" in the results


Scenario: Update a recommendation
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "name" to "desk"
    And I press the "Search" button
    Then I should see "desk" in the "name" field
    When I change "name" to "lamp"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "lamp" in the "name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "lamp" in the results
    Then I should not see "desk" in the results


Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "desk" in the results
    And I should see "mouse" in the results
    And I should see "jelly" in the results
    And I should see "tea" in the results

# Scenario: Search for dogs
#     When I visit the "Home Page"
#     And I set the "recommendation_product_name" to "chair"
#     And I press the "Search" button
#     Then I should see "desk" in the results

# Scenario: Search for available
#     When I visit the "Home Page"
#     And I select "True" in the "Activated" dropdown
#     And I press the "Search" button
#     Then I should see "desk" in the results
#     And I should see "mouse" in the results
#     And I should not see "tea" in the results

Scenario: Activate a Recommendation
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "name" to "jelly"
    And I press the "Search" button
    Then I should see "false" in the results
    And I should not see "true" in the results
    When I press the "Activate" button
    Then I should see "True" in the "Activated" dropdown
    When I set the "name" to "jelly"
    And I press the "Search" button
    Then I should see "true" in the results
    And I should not see "false" in the results

