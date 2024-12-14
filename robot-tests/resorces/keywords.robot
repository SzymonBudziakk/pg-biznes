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
    Click Button    ${ADD_TO_CART}
    Wait Until Page Contains    Product successfully added

Remove Product From Cart
    [Arguments]    ${product_name}
    Click Element    xpath://a[contains(text(), '${product_name}')]/../..${CART_REMOVE}
