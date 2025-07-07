import styles from './styles.module.css'
import cn from 'classnames'

const FormTitle = ({ loggedIn, children, className, onSubmit }) => {
  return <h2
    className={cn(styles.formTitle, className)}
    onSubmit={onSubmit}
  >
    {children}
  </h2>
}

export default FormTitle
