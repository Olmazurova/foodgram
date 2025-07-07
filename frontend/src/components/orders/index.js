import styles from './styles.module.css'
import { Icons } from '..'

const Orders = ({ orders }) => {
  if (orders === 0) { return null }
  return <div className={styles.orders}>
    <Icons.Cart />
    <span className={styles.ordersCounter}>
      {orders}
    </span>
  </div>
}

export default Orders