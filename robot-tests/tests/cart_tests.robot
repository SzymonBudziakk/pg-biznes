*** Settings ***
Library     String
Library     SeleniumLibrary
Suite Setup     Open Home Page
Suite Teardown      Close Browser

*** Variables ***
${cart_item_count}  xpath://*[@id="_desktop_cart"]/div/div/a/span[2]

${CATEGORY_ONE}    category-3
${CATEGORY_TWO}    category-6
${PRODUCT_ONE}     //article[@data-id-product="1"]//a
${PRODUCT_TWO}     //article[@data-id-product="7"]//a

${PRODUCT_COUNT_FIELD}      quantity_wanted
${SEARCH_BUTTON}            xpath://button[contains(@class, 'search')]
${ADD_TO_CART}              xpath://button[contains(@class, 'add-to-cart')]
${CLOSE}                    //*[@id="blockcart-modal"]/div/div/div[1]/button/span/i

*** Keywords ***
Open Home Page
    Open Browser   http://localhost:8080/en/    edge
    Wait Until Page Contains    Popular Products    10
    Maximize Browser Window

Search For Product
    [Arguments]    ${product_name}
    Input Text    ${SEARCH_BOX}    ${product_name}
    Click Button    ${SEARCH_BUTTON}
    Wait Until Page Contains Element    ${ADD_TO_CART}

Add Product To Cart
    [Arguments]     ${count}
    Click Element                       id=${PRODUCT_COUNT_FIELD}
    Press Keys                          id=${PRODUCT_COUNT_FIELD}   BACKSPACE
    Input Text                          id=${PRODUCT_COUNT_FIELD}   ${count}
    Click Button    ${ADD_TO_CART}
    Wait Until Page Contains    Product successfully added to your shopping cart   15
    sleep   0.5


Check Amount In Cart
    [Arguments]     ${goal}

    ${quantity_text}=                   Get Text                ${cart_item_count}
    ${quantity_text_clean}=             Remove String           ${quantity_text}           (
    ${quantity_text_clean}=             Remove String           ${quantity_text_clean}     )
    ${quantity_number}=                 Convert To Number       ${quantity_text_clean}
    Should Be Equal As Numbers          ${quantity_number}      ${goal}


*** Test Cases ***
Add 10 Products To Cart From Two Categories
    Click Element                       id=${CATEGORY_ONE}
    Wait Until Page Contains            Filter    10
    Click Element                       xpath=${PRODUCT_ONE}
    Wait Until Page Contains            Quantity
    
    Add Product To Cart                 4
    Click Element                       ${CLOSE}
    sleep   1

    Click Element                       id=${CATEGORY_TWO}
    Wait Until Page Contains            Filter    10
    Click Element                       xpath=${PRODUCT_TWO}
    Wait Until Page Contains            Quantity
    
    Add Product To Cart                 6
    Click Element                       ${CLOSE}
    sleep   1

    Check Amount In Cart                10

Search By Name And Add One Random Product
[Setup]     Add 10 Products To Cart From Two Categories
    

