import logo from './logo.svg';
import './App.css';
import Login from './components/login/login.js';
import Register from './components/register/register.js';
import Forgot from './components/forgot/forgot.js';
import Dashboard from './components/dashboard/dashboard.js';

function App() {
  return (
    <div className="App">
      <Dashboard/>
    </div>
  );
}

export default App;
