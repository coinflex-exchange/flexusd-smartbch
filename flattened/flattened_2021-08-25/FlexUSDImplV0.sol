// SPDX-License-Identifier: MIT

pragma solidity 0.8.4;



// Part: Context

/**
 * @dev Provides information about the current execution context, including the
 * sender of the transaction and its data. While these are generally available
 * via msg.sender and msg.data, they should not be accessed in such a direct
 * manner, since when dealing with meta-transactions the account sending and
 * paying for execution may not be the actual sender (as far as an application
 * is concerned).
 *
 * This contract is only required for intermediate, library-like contracts.
 */
abstract contract Context {
  function _msgSender() internal view virtual returns (address) {
    return msg.sender;
  }

  function _msgData() internal view virtual returns (bytes calldata) {
    return msg.data;
  }
}

// Part: IERC20

interface IERC20 {
  /**
   * @dev Returns the amount of tokens in existence.
   */
  function totalSupply() external view returns (uint256);

  /**
   * @dev Returns the amount of tokens owned by `account`.
   */
  function balanceOf(address account) external view returns (uint256);

  /**
   * @dev Moves `amount` tokens from the caller's account to `recipient`.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transfer(address recipient, uint256 amount) external returns (bool);

  /**
   * @dev Returns the remaining number of tokens that `spender` will be
   * allowed to spend on behalf of `owner` through {transferFrom}. This is
   * zero by default.
   *
   * This value changes when {approve} or {transferFrom} are called.
   */
  function allowance(address owner, address spender) external view returns (uint256);

  /**
   * @dev Sets `amount` as the allowance of `spender` over the caller's tokens.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * IMPORTANT: Beware that changing an allowance with this method brings the risk
   * that someone may use both the old and the new allowance by unfortunate
   * transaction ordering. One possible solution to mitigate this race
   * condition is to first reduce the spender's allowance to 0 and set the
   * desired value afterwards:
   * https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
   *
   * Emits an {Approval} event.
   */
  function approve(address spender, uint256 amount) external returns (bool);

  /**
   * @dev Moves `amount` tokens from `sender` to `recipient` using the
   * allowance mechanism. `amount` is then deducted from the caller's
   * allowance.
   *
   * Returns a boolean value indicating whether the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

  /**
   * @dev Emitted when `value` tokens are moved from one account (`from`) to
   * another (`to`).
   *
   * Note that `value` may be zero.
   */
  event Transfer(address indexed from, address indexed to, uint256 value);

  /**
   * @dev Emitted when the allowance of a `spender` for an `owner` is set by
   * a call to {approve}. `value` is the new allowance.
   */
  event Approval(address indexed owner, address indexed spender, uint256 value);
}

// Part: SafeMath

/**
 * @dev Wrappers over Solidity's arithmetic operations.
 * @notice CAUTION
 * This version of SafeMath should only be used with Solidity 0.8 or later,
 * because it relies on the compiler's built in overflow checks.
 *
 * NOTE: `SafeMath` is no longer needed starting with Solidity 0.8. The compiler
 * now has built in overflow checking.
 */
library SafeMath {
  /**
   * @dev Returns the addition of two unsigned integers, with an overflow flag.
   *
   * _Available since v3.4._
   */
  function tryAdd(uint256 a, uint256 b)
    internal pure returns (bool, uint256)
  {
    unchecked {
      uint256 c = a + b;
      if (c < a) return (false, 0);
      return (true, c);
    }
  }

  /**
   * @dev Returns the substraction of two unsigned integers, with an overflow flag.
   *
   * _Available since v3.4._
   */
  function trySub(uint256 a, uint256 b)
    internal pure returns (bool, uint256)
  {
    unchecked {
      if (b > a) return (false, 0);
      return (true, a - b);
    }
  }

  /**
   * @dev Returns the multiplication of two unsigned integers, with an overflow flag.
   *
   * _Available since v3.4._
   */
  function tryMul(uint256 a, uint256 b)
    internal pure returns (bool, uint256)
  {
    unchecked {
      // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
      // benefit is lost if 'b' is also tested.
      // See: https://github.com/OpenZeppelin/openzeppelin-contracts/pull/522
      if (a == 0) return (true, 0);
      uint256 c = a * b;
      if (c / a != b) return (false, 0);
      return (true, c);
    }
  }

  /**
   * @dev Returns the division of two unsigned integers, with a division by zero flag.
   *
   * _Available since v3.4._
   */
  function tryDiv(uint256 a, uint256 b)
    internal pure returns (bool, uint256)
  {
    unchecked {
      if (b == 0) return (false, 0);
      return (true, a / b);
    }
  }

  /**
   * @dev Returns the remainder of dividing two unsigned integers, with a division by zero flag.
   *
   * _Available since v3.4._
   */
  function tryMod(uint256 a, uint256 b)
    internal pure returns (bool, uint256)
  {
    unchecked {
      if (b == 0) return (false, 0);
      return (true, a % b);
    }
  }

  /**
   * @dev Returns the addition of two unsigned integers, reverting on
   * overflow.
   *
   * Counterpart to Solidity's `+` operator.
   *
   * Requirements:
   *
   * - Addition cannot overflow.
   */
  function add(uint256 a, uint256 b)
    internal pure returns (uint256)
  {
    return a + b;
  }

  /**
   * @dev Returns the subtraction of two unsigned integers, reverting on
   * overflow (when the result is negative).
   *
   * Counterpart to Solidity's `-` operator.
   *
   * Requirements:
   *
   * - Subtraction cannot overflow.
   */
  function sub(uint256 a, uint256 b)
    internal pure returns (uint256)
  {
    return a - b;
  }

  /**
   * @dev Returns the multiplication of two unsigned integers, reverting on
   * overflow.
   *
   * Counterpart to Solidity's `*` operator.
   *
   * Requirements:
   *
   * - Multiplication cannot overflow.
   */
  function mul(uint256 a, uint256 b)
    internal pure returns (uint256)
  {
    return a * b;
  }

  /**
   * @dev Returns the integer division of two unsigned integers, reverting on
   * division by zero. The result is rounded towards zero.
   *
   * Counterpart to Solidity's `/` operator.
   *
   * Requirements:
   *
   * - The divisor cannot be zero.
   */
  function div(uint256 a, uint256 b)
    internal pure returns (uint256)
  {
    return a / b;
  }

  /**
   * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
   * reverting when dividing by zero.
   *
   * Counterpart to Solidity's `%` operator. This function uses a `revert`
   * opcode (which leaves remaining gas untouched) while Solidity uses an
   * invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   *
   * - The divisor cannot be zero.
   */
  function mod(uint256 a, uint256 b)
    internal pure returns (uint256)
  {
    return a % b;
  }

  /**
   * @dev Returns the subtraction of two unsigned integers, reverting with custom message on
   * overflow (when the result is negative).
   *
   * CAUTION: This function is deprecated because it requires allocating memory for the error
   * message unnecessarily. For custom revert reasons use {trySub}.
   *
   * Counterpart to Solidity's `-` operator.
   *
   * Requirements:
   *
   * - Subtraction cannot overflow.
   */
  function sub(uint256 a, uint256 b, string memory errorMessage)
    internal pure returns (uint256)
  {
    unchecked {
      require(b <= a, errorMessage);
      return a - b;
    }
  }

  /**
   * @dev Returns the integer division of two unsigned integers, reverting with custom message on
   * division by zero. The result is rounded towards zero.
   *
   * Counterpart to Solidity's `/` operator. Note: this function uses a
   * `revert` opcode (which leaves remaining gas untouched) while Solidity
   * uses an invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   *
   * - The divisor cannot be zero.
   */
  function div(uint256 a, uint256 b, string memory errorMessage)
    internal pure returns (uint256)
  {
    unchecked {
      require(b > 0, errorMessage);
      return a / b;
    }
  }

  /**
   * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
   * reverting with custom message when dividing by zero.
   *
   * CAUTION: This function is deprecated because it requires allocating memory for the error
   * message unnecessarily. For custom revert reasons use {tryMod}.
   *
   * Counterpart to Solidity's `%` operator. This function uses a `revert`
   * opcode (which leaves remaining gas untouched) while Solidity uses an
   * invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   *
   * - The divisor cannot be zero.
   */
  function mod(uint256 a, uint256 b, string memory errorMessage)
    internal pure returns (uint256)
  {
    unchecked {
      require(b > 0, errorMessage);
      return a % b;
    }
  }
}

// Part: Ownable

/**
 * @dev Contract module which provides a basic access control mechanism, where
 * there is an account (an owner) that can be granted exclusive access to
 * specific functions.
 *
 * By default, the owner account will be the one that deploys the contract. This
 * can later be changed with {transferOwnership}.
 *
 * This module is used through inheritance. It will make available the modifier
 * `onlyOwner`, which can be applied to your functions to restrict their use to
 * the owner.
 */
abstract contract Ownable is Context {
  address private _owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  /**
   * @dev Initializes the contract setting the deployer as the initial owner.
   */
  constructor() {
    _setOwner(_msgSender());
  }

  /**
   * @dev Returns the address of the current owner.
   */
  function owner() public view virtual returns(address) {
    return _owner;
  }

  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(owner() == _msgSender(), 'Ownable: caller is not the owner');
    _;
  }

  /**
   * @dev Leaves the contract without owner. It will not be possible to call
   * `onlyOwner` functions anymore. Can only be called by the current owner.
   *
   * NOTE: Renouncing ownership will leave the contract without an owner,
   * thereby removing any functionality that is only available to the owner.
   */
  function renounceOwnership() public virtual onlyOwner {
    _setOwner(address(0));
  }

  /**
   * @dev Transfers ownership of the contract to a new account (`newOwner`).
   * Can only be called by the current owner.
   */
  function transferOwnership(address newOwner) public virtual onlyOwner {
    require(newOwner != address(0), 'Ownable: new owner is the zero address');
    _setOwner(newOwner);
  }

  function _setOwner(address newOwner) private {
    address oldOwner = _owner;
    _owner = newOwner;
    emit OwnershipTransferred(oldOwner, newOwner);
  }
}

// Part: flexUSDStorage

/**
 * Storage Abstract Contract, do not change
 */
abstract contract flexUSDStorage is Ownable {
  /**
   * Member Variable(s)
   */
  bool public initialized;

  mapping(address => uint256) internal _balances;
  mapping(address => mapping(address => uint256)) internal _allowances;
  mapping(address => bool) public blacklist;
  uint256 internal _totalSupply;
  string public constant name   = 'flexUSD';
  string public constant symbol = 'flexUSD';
  uint256 public multiplier;
  uint8 public constant decimals = 18;
  uint256 internal constant deci = 1e18;
  bool internal getpause;
}

// Part: LibraryLock

contract LibraryLock is flexUSDStorage {
  // Ensures no one can manipulate the Logic Contract once it is deployed.
  // PARITY WALLET HACK PREVENTION

  modifier delegatedOnly()
  {
    require(initialized == true, "The library is locked. No direct 'call' is allowed.");
    _;
  }

  function initialize()
    internal
  {
    initialized = true;
  }
}

// File: flexUSDImplV0.sol

contract flexUSDImplV0 is Context, flexUSDStorage, LibraryLock, IERC20
{
  using SafeMath for uint256;
  /**
   * Event(s)
   */
  event fTokenBlacklist(address indexed account, bool blocked);
  event ChangeMultiplier(uint256 multiplier);
  event CodeUpdated(address indexed newCode);

  function initialize(uint256 _totalsupply)
    public
  {
    require(!initialized, 'The library has already been initialized.');	
    LibraryLock.initialize();
    multiplier = 1 * deci;
    _totalSupply = _totalsupply;
    _balances[msg.sender] = _totalSupply;
  }

  function setMultiplier(uint256 _multiplier)
    external onlyOwner isPaused
  {
    require(_multiplier > multiplier, 'the multiplier should be greater than previous multiplier');
    multiplier = _multiplier;
    emit ChangeMultiplier(multiplier);
  }

  function totalSupply()
    public override view returns (uint256)
  {
    return _totalSupply.mul(multiplier).div(deci);
  }

  function setTotalSupply(uint256 inputTotalsupply)
    external onlyOwner
  {
    require(inputTotalsupply > totalSupply(), 'the input total supply is not greater than present total supply');
    multiplier = (inputTotalsupply.mul(deci)).div(_totalSupply);
    emit ChangeMultiplier(multiplier);
  }

  function balanceOf(address account)
    public override view returns (uint256)
  {
    uint256 externalAmt;
    externalAmt = _balances[account].mul(multiplier).div(deci);
    return externalAmt;
  }

  function transfer(address recipient, uint256 amount)
    public virtual override
    notBlacklisted(msg.sender) notBlacklisted(recipient) isPaused
    returns (bool)
  {
    uint256 internalAmt;
    uint256 externalAmt = amount;
    internalAmt = (amount.mul(deci)).div(multiplier);
    _transfer(msg.sender, recipient, externalAmt);
    return true;
  }

  function allowance(address owner, address spender)
    public virtual override view returns (uint256)
  {
    uint256 externalAmt;
    uint256 maxapproval = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    maxapproval = maxapproval.div(multiplier).mul(deci);
    if (_allowances[owner][spender] > maxapproval)
    {
      externalAmt = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    } else {
      externalAmt = (_allowances[owner][spender]).mul(multiplier).div(deci);
    }
    return externalAmt;
  }

  function approve(address spender, uint256 amount)
    public virtual override
    notBlacklisted(spender) notBlacklisted(msg.sender) isPaused
    returns (bool)
  {
    uint256 internalAmt;
    uint256 externalAmt = amount;
    internalAmt = externalAmt.mul(deci).div(multiplier);
    _approve(msg.sender, spender, externalAmt);
    return true;
  }
  
  /**
   * @dev Atomically increases the allowance granted to `spender` by the caller.
   *
   * This is an alternative to {approve} that can be used as a mitigation for
   * problems described in {IERC20-approve}.
   *
   * Emits an {Approval} event indicating the updated allowance.
   *
   * Requirements:
   *
   * - `spender` cannot be the zero address.
   */
  function increaseAllowance(address spender, uint256 addedValue) public 
    notBlacklisted(spender) notBlacklisted(msg.sender) isPaused
    returns (bool) 
  {
    uint256 externalAmt = allowance(_msgSender(),spender);
    _approve(_msgSender(), spender, externalAmt.add(addedValue));
    return true;
  }

  /**
   * @dev Atomically decreases the allowance granted to `spender` by the caller.
   *
   * This is an alternative to {approve} that can be used as a mitigation for
   * problems described in {IERC20-approve}.
   *
   * Emits an {Approval} event indicating the updated allowance.
   *
   * Requirements:
   *
   * - `spender` cannot be the zero address.
   * - `spender` must have allowance for the caller of at least
   * `subtractedValue`.
   */
  function decreaseAllowance(address spender, uint256 subtractedValue)
    public notBlacklisted(spender) notBlacklisted(msg.sender) isPaused returns (bool)
  {
    uint256 externalAmt = allowance(_msgSender(),spender) ;
    _approve(_msgSender(), spender, externalAmt.sub(subtractedValue, 'ERC20: decreased allowance below zero'));
    return true;
  }

  function transferFrom(address sender, address recipient, uint256 amount)
    public virtual override
    notBlacklisted(sender) notBlacklisted(msg.sender) notBlacklisted(recipient) isPaused
    returns (bool)
  {
    uint256 externalAmt = allowance(sender,_msgSender());
    _transfer(sender, recipient, amount);
    _approve(sender, _msgSender(),
      externalAmt.sub(amount, 'ERC20: transfer amount exceeds allowance')
    );
    return true;
  }

  function _transfer(address sender, address recipient, uint256 externalAmt)
    internal virtual
  {
    require(sender != address(0), 'ERC20: transfer from the zero address');
    require(recipient != address(0), 'ERC20: transfer to the zero address');
    uint256 internalAmt = externalAmt.mul(deci).div(multiplier);
    _balances[sender] = _balances[sender].sub(
      internalAmt, 'ERC20: transfer internalAmt exceeds balance'
    );
    _balances[recipient] = _balances[recipient].add(internalAmt);
    emit Transfer(sender, recipient, externalAmt);
  }

  function mint(address mintTo, uint256 amount)
    public virtual onlyOwner isPaused returns (bool)
  {
    uint256 externalAmt = amount;
    uint256 internalAmt = externalAmt.mul(deci).div(multiplier);
    _mint(mintTo, internalAmt, externalAmt);
    return true;
  }

  function _mint(address account, uint256 internalAmt, uint256 externalAmt)
    internal virtual
  {
    require(account != address(0), 'ERC20: mint to the zero address');
    _totalSupply = _totalSupply.add(internalAmt);
    _balances[account] = _balances[account].add(internalAmt);
    emit Transfer(address(0), account, externalAmt);
  }

  function burn(address burnFrom, uint256 amount)
    public virtual onlyOwner isPaused returns (bool)
  {
    uint256 internalAmt;
    uint256 externalAmt = amount;
    internalAmt = externalAmt.mul(deci).div(multiplier);
    _burn(burnFrom, internalAmt, externalAmt);
    return true;
  }

  function _burn(address account, uint256 internalAmt, uint256 externalAmt)
    internal virtual
  {
    require(account != address(0), 'ERC20: burn from the zero address');
    _balances[account] = _balances[account].sub(
      internalAmt, 'ERC20: burn internaAmt exceeds balance'
    );
    _totalSupply = _totalSupply.sub(internalAmt);
    emit Transfer(account, address(0), externalAmt);
  }

  function _approve(address owner, address spender, uint256 externalAmt)
    internal virtual
  {
    require(owner != address(0), 'ERC20: approve from the zero address');
    require(spender != address(0), 'ERC20: approve to the zero address');
    uint256 internalAmt = externalAmt.mul(deci).div(multiplier);
    uint256 maxapproval = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    maxapproval = maxapproval.div(multiplier).mul(deci);
    if (internalAmt > maxapproval)
    {
      internalAmt = maxapproval;
    }
    _allowances[owner][spender] = internalAmt;
    emit Approval(owner, spender, externalAmt);
  }

  function pause()
    external onlyOwner
  {
    getpause = true;
  }

  function unpause()
    external onlyOwner
  {
    getpause = false;
  }

  // pause unpause

  modifier isPaused()
  {
    require(getpause == false, 'the contract is paused');
    _;
  }

  // blacklisting account

  function addToBlacklist(address account)
    external onlyOwner
  {
    blacklist[account] = true;
    emit fTokenBlacklist(account, true);
  }

  function removeFromBlacklist(address account)
    external onlyOwner
  {
    blacklist[account] = false;
    emit fTokenBlacklist(account, false);
  }

  modifier notBlacklisted(address account) {
    require(!blacklist[account], 'account is blacklisted');
    _;
  }
}
