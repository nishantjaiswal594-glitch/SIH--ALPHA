export default function Toast({ type = 'info', children, onClose }) {
  return <div className={`toast toast-${type}`} role="status"><span>{children}</span>{onClose && <button onClick={onClose}>×</button>}</div>
}
