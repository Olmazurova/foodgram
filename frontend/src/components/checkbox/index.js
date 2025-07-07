import cn from 'classnames'
import styles from './styles.module.css'
import { useState } from 'react'
import { Icons } from '../index'
import { hexToRgba } from '../../utils'

const Checkbox = ({
  onChange,
  className,
  color,
  value = false,
  name,
  id
}) => {
  const clickHandler = () => {
    onChange && onChange(id)
  }
  const classNames = cn(styles['checkbox-container'], className, {
    [styles['checkbox_active']]: value
  })

  return <div className={classNames} onClick={clickHandler}>
    {name}
  </div>
}


export default Checkbox