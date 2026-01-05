// SPDX - License - Identifier: MIT
pragma
solidity ^ 0.8
.0;

/ **
* @ title
EmperorToken
* @ dev
Standard
ERC20
token
for Emperor Blockchain
    * /
    contract
    EmperorToken
    {
        string
    public
    constant
    name = "Emperor Token";
    string
    public
    constant
    symbol = "EMPEROR";
    uint8
    public
    constant
    decimals = 18;
    uint256
    public
    totalSupply;

    mapping(address= > uint256) private
    balances;
    mapping(address= > mapping(address= > uint256)) private
    allowances;

    event
    Transfer(address
    indexed
    from, address
    indexed
    to, uint256
    value);
    event
    Approval(address
    indexed
    owner, address
    indexed
    spender, uint256
    value);

    / **
    * @ dev
    Constructor
    that
    gives
    msg.sender
    all
    existing
    tokens
    * @ param
    initialSupply
    The
    initial
    supply
    of
    tokens
    * /
    constructor(uint256
    initialSupply) {
        totalSupply = initialSupply;
    balances[msg.sender] = initialSupply;
    emit
    Transfer(address(0), msg.sender, initialSupply);
    }

    / **
    * @ dev
    Get
    the
    balance
    of
    the
    specified
    address
    * @ param
    _owner
    The
    address
    to
    query
    the
    balance
    of
    * @
    return balance
    The
    balance
    amount
    * /
    function
    balanceOf(address
    _owner) public
    view
    returns(uint256
    balance) {
    return balances[_owner];
    }

    / **
    * @ dev
    Transfer
    token
    to
    a
    specified
    address
    * @ param
    _to
    The
    address
    to
    transfer
    to
    * @ param
    _value
    The
    amount
    to
    be
    transferred
    * @
    return success
    Whether
    the
    transfer
    was
    successful
    * /
    function
    transfer(address
    _to, uint256
    _value) public
    returns(bool
    success) {
        require(balances[msg.sender] >= _value, "Insufficient balance");

    balances[msg.sender] -= _value;
    balances[_to] += _value;

    emit
    Transfer(msg.sender, _to, _value);
    return true;
    }

    / **
    * @ dev
    Transfer
    tokens
    from one address

    to
    another
    * @ param
    _from
    The
    address
    to
    transfer
    from
    * @ param
    _to
    The
    address
    to
    transfer
    to
    * @ param
    _value
    The
    amount
    to
    be
    transferred
    * @
    return success
    Whether
    the
    transfer
    was
    successful
    * /
    function
    transferFrom(address
    _from, address
    _to, uint256
    _value) public
    returns(bool
    success) {
        require(balances[_from] >= _value, "Insufficient balance");
    require(allowances[_from][msg.sender] >= _value, "Allowance exceeded");

    balances[_from] -= _value;
    balances[_to] += _value;
    allowances[_from][msg.sender] -= _value;

    emit
    Transfer(_from, _to, _value);
    return true;
    }

    / **
    * @ dev
    Approve
    the
    passed
    address
    to
    spend
    the
    specified
    amount
    of
    tokens
    * @ param
    _spender
    The
    address
    which
    will
    spend
    the
    funds
    * @ param
    _value
    The
    amount
    of
    tokens
    to
    be
    spent
    * @
    return success
    Whether
    the
    approval
    was
    successful
    * /
    function
    approve(address
    _spender, uint256
    _value) public
    returns(bool
    success) {
        allowances[msg.sender][_spender] = _value;
    emit
    Approval(msg.sender, _spender, _value);
    return true;
    }

    / **
    * @ dev
    Get
    the
    amount
    of
    tokens
    approved
    for spending
        * @ param _owner The address that owns the tokens
    * @ param _spender The address that will spend the tokens
    * @
    return remaining
    The
    amount
    of
    tokens
    still
    available
    for the spender
        * /
        function
        allowance(address
        _owner, address
        _spender) public
        view
        returns(uint256
        remaining) {
        return allowances[_owner][_spender];
        }
        }