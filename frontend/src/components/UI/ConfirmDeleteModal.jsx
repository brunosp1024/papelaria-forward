import './ConfirmDeleteModal.css';
import React from 'react';


function Modal({ show, onClose, children }) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (show && ref.current) {
      void ref.current.offsetWidth;
      ref.current.classList.add('show');
    }
  }, [show]);
  if (!show) return null;
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };
  return (
    <div className="modal-backdrop-custom" ref={ref} onMouseDown={handleBackdropClick}>
      <div className="modal-custom">
        {children}
        <button className="modal__close" onClick={onClose} aria-label="Fechar">×</button>
      </div>
    </div>
  );
}

function Button({ variant, onClick, children, ...props }) {
  const color = variant === 'danger' ? 'red' : variant === 'secondary' ? 'gray' : 'blue';
  return (
    <button
      className={`btn btn--${variant}`}
      style={{ backgroundColor: color, color: 'white', border: 'none', borderRadius: 4, padding: '8px 16px', marginLeft: 8 }}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
}


const ConfirmeDeleteModal = ({ show, handleClose, onConfirm }) => {
  return (
    <Modal show={show} onClose={handleClose}>
      <div className="modal__header" style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
        <svg style={{ fontSize: 28, color: 'red', width: 28, height: 28 }} viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
          <rect x="11" y="7" width="2" height="7" rx="1" fill="currentColor" />
          <rect x="11" y="16" width="2" height="2" rx="1" fill="currentColor" />
        </svg>
        <span style={{ fontWeight: 700, fontSize: 20 }}>Excluir item</span>
      </div>
      <div className="modal__body" style={{ marginBottom: 16 }}>
        Essa venda será excluída permanentemente com todos os seus itens. Deseja continuar?
      </div>
      <div className="modal__footer" style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button variant="secondary" onClick={handleClose}>
          Cancelar
        </Button>
        <Button variant="danger" onClick={onConfirm}>
          Confirmar
        </Button>
      </div>
    </Modal>
  );
};

export default ConfirmeDeleteModal;