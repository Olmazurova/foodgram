import styles from './styles.module.css'
import cn from 'classnames'

const Tag = ({ name, className }) => {
  return <div className={cn(styles.tag, className)}>
    {name}
  </div>
}

export default Tag
