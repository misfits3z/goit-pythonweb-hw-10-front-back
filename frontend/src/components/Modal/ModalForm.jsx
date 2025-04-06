
import css from './ModalForm.module.css';

const ModalForm = ({ children, onClose }) => {
  return (
    <div className={css.backdrop} onClick={onClose}>
      <div className={css.modal} onClick={(e) => e.stopPropagation()}>
        <button className={css.closeBtn} onClick={onClose}>×</button>
        {children}
      </div>
    </div>
  );
};

export default ModalForm;