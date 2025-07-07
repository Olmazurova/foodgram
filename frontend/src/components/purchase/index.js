import styles from './styles.module.css'
import { LinkComponent, Icons, Popup } from '../index'
import { useState } from 'react'
import cn from 'classnames'

const Purchase = ({
  image,
  name,
  cooking_time,
  id,
  handleRemoveFromCart,
  is_in_shopping_cart,
  updateOrders,
  ingredients
}) => {
  const [ expanded, setExpanded ] = useState(false)
  const [ toDelete, setToDelete ] = useState(false)
  if (!is_in_shopping_cart) { return null }

  return <li className={styles.purchase}>
    {toDelete && <Popup
      title='Вы уверены, что хотите удалить рецепт?'
      onSubmit={() => {
        handleRemoveFromCart({
          id,
          toAdd: false,
          callback: () => {
            updateOrders()
            setToDelete(false)
          }
        })
      }}
      onClose={() => {
        setToDelete(false)
      }}
    />}
    <div className={styles.purchaseBody}>
      <div className={styles.purchaseContent}>
        <div
          alt={name}
          className={styles.purchaseImage}
          style={{
            backgroundImage: `url(${image})`
          }}
        />
        <h3 className={styles.purchaseTitle}>
          <LinkComponent className={styles.recipeLink} title={name} href={`/recipes/${id}`} />
          <div className={cn(styles.purchaseExpandButton, {
            [styles.purchaseExpandButtonExpanded]: expanded
          })} onClick={() => setExpanded(!expanded)}>
            <Icons.ArrowExpand />
          </div>
        </h3>
        <p className={styles.purchaseText}>
          {cooking_time} мин.
        </p>
      </div>
      <a
        href="#"
        className={styles.purchaseDelete}
        onClick={_ => setToDelete(true)}
      >
        <Icons.ReceiptDelete />
      </a>
    </div>
    {expanded && ingredients && ingredients.length > 0 && <ul className={styles.purchaseIngredients}>
      {ingredients.map(ingredient => {
      return <li>{ingredient.name}</li>
      })}
    </ul>}
    
  </li>
}

export default Purchase
