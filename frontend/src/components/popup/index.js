import styles from './styles.module.css'
import { Icons, Button } from '..'

const Popup = ({
  title,
  onSubmit,
  onClose
}) => {

  return <div className={styles.popup} onClick={e => {
    if (e.target === e.currentTarget) {
      onClose && onClose()
    }
  }}>
    <div className={styles.popup__content}>
      <div className={styles.popup__close} onClick={onClose}>
        <Icons.PopupClose />
      </div>
      <h3 className={styles.popup__title}>{title}</h3>
      {onSubmit && <div className={styles.popup__buttons}>
        <Button
          className={styles.popup__button}
          clickHandler={onSubmit}
        >
          Да
        </Button>
        <Button
          clickHandler={onClose}
          className={styles.popup__button}
        >
          Нет
        </Button>
      </div>}
    </div>
  </div>
}

export default Popup