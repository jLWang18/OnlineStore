
const SignUp = () => {
    return (
    <div>
    <form>
    <div className="input-control">
      <label htmlFor="fname">First Name</label>
      <input type="text" id="fname" name="fname"/>
    </div>
    <br/><br/>
    <div className="input-control">
      <label htmlFor="lname">Last Name</label>
      <input type="text" id="lname" name="lname"/>
    </div>
    <br/><br/>
    <div className="input-control">
      <label htmlFor="email">Email</label>
      <input type="text" id="email" name="email"/>
    </div>
    <div className="input-control">
      <label htmlFor="password">Password</label>
      <input type="text" id="password" name="password"/>
    </div>
    <br/><br/>
    <div className="input-control">
      <label htmlFor="phone">Phone</label>
      <input type="text" id="phone" name="phone"/>
    </div>
    <br/><br/>
    <button type="submit">Sign up</button>
    </form>
    </div>
    )
  }

  export default SignUp