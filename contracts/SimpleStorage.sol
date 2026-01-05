// SPDX - License - Identifier: MIT
pragma
solidity ^ 0.8
.0;

/ **
* @ title
SimpleStorage
* @ dev
Store & retrieve
value in a
variable
* /
contract
SimpleStorage
{
    uint256
storedData;

/ **
* @ dev
Store
value in variable
* @ param
_value
value
to
store
* /
function
set(uint256
_value) public
{
    storedData = _value;
}

/ **
* @ dev
Return
value
* @
return value
of
'storedData'
* /
function
get()
public
view
returns(uint256)
{
return storedData;
}
}