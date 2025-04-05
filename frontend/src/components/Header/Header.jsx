
import css from './Header.module.css';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../redux/auth/authSlice';
import { selectIsAuthenticated } from '../../redux/auth/authSelectors';


const Header = () => {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <header className={css.header}>
      <h1 className={css.title}>Phonebook</h1>
      <nav>
        {isAuthenticated ? (
          <button onClick={handleLogout} className={css.btn}>Logout</button>
        ) : (
          <>
            <button className={css.btn}>Login</button>
            <button className={css.btn}>Register</button>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;