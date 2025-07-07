import styles from './style.module.css'
import { Nav, AccountMenu, LinkComponent } from '../index.js'
import Container from '../container'
import LogoHeader from '../../images/logo-header.png'

const Header = ({ loggedIn, onSignOut, orders }) => {
  return <header className={styles.header}>
    <Container>
      <div className={styles.headerContent}>
        <LinkComponent
          className={styles.headerLink}
          title={<img className={styles.headerLogo} src={LogoHeader} alt='Foodgram' />}
          href='/'
        />
        <Nav
          loggedIn={loggedIn}
          onSignOut={onSignOut}
          orders={orders}
        />
      </div>
    </Container>
  </header>
}

export default Header
