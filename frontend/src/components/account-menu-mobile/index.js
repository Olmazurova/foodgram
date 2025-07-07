import styles from './styles.module.css'
import { useContext } from 'react'
import { LinkComponent, AccountMobile, Button } from '../index.js'
import { AuthContext } from '../../contexts'
import { useLocation } from 'react-router-dom'
import { NotLoggedInMenu } from '../../configs/navigation'

const AccountMenuMobile = ({ onSignOut, orders }) => {
  const authContext = useContext(AuthContext)
  const location = useLocation()
  if (!authContext) {
    return <div className={styles.menu}>
      {NotLoggedInMenu.map(item => {
        return location.pathname === item.href ? <Button
          href={item.href}
          modifier='style_dark'
          className={styles.menuButton}
        >
          {item.title}
        </Button> : <LinkComponent
          title={item.title}
          href={item.href}
          exact
          className={styles.menuLink}
        />
      })}
    </div>
  }
  return <div className={styles.menu}>
    <AccountMobile onSignOut={onSignOut} orders={orders} />
  </div>
}


export default AccountMenuMobile