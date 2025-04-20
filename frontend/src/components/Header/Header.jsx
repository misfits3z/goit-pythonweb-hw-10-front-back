
import css from './Header.module.css';
import { useSelector, useDispatch } from 'react-redux';
import { logout } from '../../redux/auth/authSlice';
import { selectIsAuthenticated } from '../../redux/auth/authSelectors';
import { useState } from 'react';
import ModalForm from '../Modal/ModalForm'
import LoginForm from '../LoginForm/LoginForm'
import { Link } from "react-router-dom";
import Logo from '../../images/Logo.svg'




const Header = () => {
  const isAuthenticated = useSelector(selectIsAuthenticated);
  const dispatch = useDispatch();

  const [modalType, setModalType] = useState(null);

  const handleLogout = () => {
    dispatch(logout());
  };

  const openModal = (type) => setModalType(type);
  const closeModal = () => setModalType(null);



  return (
    <header className={css.header}>
      
      <Link className={css.logo} to="/">     
        <img src={Logo} width="136" height="15" />
      </Link>
      <nav>
        {isAuthenticated ? (
          <button onClick={handleLogout} className={css.btn}>Logout</button>
        ) : (
          <>
            <button className={css.btn} onClick={() => openModal('login')}>Login</button>
            
          </>
        )}
      </nav>

      {modalType && (
        <ModalForm onClose={closeModal}>
          {modalType === 'login' && <LoginForm onClose={closeModal} />}
        </ModalForm>
      )}

    </header>
  );
};

export default Header;