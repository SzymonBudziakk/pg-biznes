*** Settings ***
Library     String
Library     helpers.py
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
    Click Button                        ${ADD_TO_CART}
    Wait Until Page Contains            Product successfully added to your shopping cart   30
    sleep   2
    Click Element                       ${CLOSE}
    sleep   2

Check Amount In Cart
    [Arguments]     ${goal}

    ${quantity_text}=                   Get Text                ${cart_item_count}
    ${quantity_text_clean}=             Remove String           ${quantity_text}           (
    ${quantity_text_clean}=             Remove String           ${quantity_text_clean}     )
    ${quantity_number}=                 Convert To Number       ${quantity_text_clean}
    Should Be Equal As Numbers          ${quantity_number}      ${goal}

Add 10 Products To Cart From Two Categories
    Click Element                       id=${CATEGORY_ONE}
    Wait Until Page Contains            Filter    10
    Click Element                       xpath=${PRODUCT_ONE}
    Wait Until Page Contains            Quantity
    
    Add Product To Cart                 3
    
    Click Element                       id=${CATEGORY_TWO}
    Wait Until Page Contains            Filter    10
    Click Element                       xpath=${PRODUCT_TWO}
    Wait Until Page Contains            Quantity
    
    Add Product To Cart                 7

    Check Amount In Cart                10

Search By Name And Add One Random Product
    Input Text                      //*[@id="search_widget"]/form/input[2]  bird
    Press Keys                      //*[@id="search_widget"]/form/input[2]  ENTER
    Wait Until Page Contains        Search results  15
    ${product_links}=               Get WebElements    css:.products .product a.thumbnail.product-thumbnail
    ${random_product}=              Select Random Element    ${product_links}
    ${product_url}=                 Get Element Attribute    ${random_product}    href
    Click Element                   ${random_product}
    Add Product To Cart             1

Remove Three Products From Cart
    Click Element                               xpath=//*[@id="_desktop_cart"]/div/div/a
    Wait Until Page Contains                    Shopping Cart   10
    Click Element                               xpath=//*[@id="main"]/div/div[1]/div/div[2]/ul/li[1]/div/div[3]/div/div[3]/div/a

Register New Account
    Click Element                               xpath=//*[@id="_desktop_user_info"]/div/a
    Wait Until Page Contains                    Log in to your account   10
    Click Element                               xpath=//*[@id="content"]/div/a
    Wait Until Page Contains                    Create an account   10
    Click Button                                id=field-id_gender-2
    Input Text                                  //*[@id="field-firstname"]  Len
    Input Text                                  //*[@id="field-lastname"]  Kingodysey
    
    ${random_number}=                           Generate Random String      7    0123456789
    Input Text                                  //*[@id="field-email"]  Example${random_number}@gmail.com
    Input Text                                  //*[@id="field-password"]   jedzOwoce1Warzywa
    Click Button                                //*[@id="customer-form"]/div/div[8]/div[1]/span/label/input
    Click Button                                //*[@id="customer-form"]/div/div[10]/div[1]/span/label/input
    Click Button                                //*[@id="customer-form"]/footer/button
    Wait Until Element Is Visible               //*[@id="_desktop_user_info"]/div/a[1]
    sleep   10

Make Order
    Click Element                               //*[@id="_desktop_cart"]/div/div/a
    Wait Until Page Contains                    Shopping Cart   10
    Click Element                               xpath=//*[@id="main"]/div/div[2]/div[1]/div[2]/div/a

    Wait Until Page Contains                    Addresses   10
    Input Text                                  //*[@id="field-address1"]       SomeCoolAdress 85
    Input Text                                  //*[@id="field-postcode"]       13-111
    Input Text                                  //*[@id="field-city"]           PgCity
    Select From List By Value                   //*[@id="field-id_country"]     14
    Click Button                                //*[@id="delivery-address"]/div/footer/button

    Wait Until Page Contains                    Pick up in-store   10
    Click Button                                //*[@id="js-delivery"]/button

    Wait Until Page Contains                    bank wire   10 
    Click Button                                //*[@id="payment-option-2"]
    Click Button                                //*[@id="conditions_to_approve[terms-and-conditions]"]  
    Click Button                                //*[@id="payment-confirmation"]/div[1]/button

    Wait Until Page Contains                    Your order is confirmed   10 
    Click Element                               xpath=//*[@id="_desktop_user_info"]/div/a[2]/span
    Wait Until Page Contains                    Your account    10
    Click Element                               //*[@id="history-link"]
    Wait Until Page Contains                    Awaiting bank wire payment  10

*** Test Cases ***

Cart Test
    Register New Account
    Add 10 Products To Cart From Two Categories
    Search By Name And Add One Random Product
    Remove Three Products From Cart
    Wait Until Keyword Succeeds    15 sec   1 sec   Check Amount In Cart    8
    Make Order