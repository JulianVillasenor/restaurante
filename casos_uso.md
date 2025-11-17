# Casos de uso – Sistema de Restaurante  
**Entidades clave:** Mesa, Cuenta, Venta, Producto  

---

## 1. Descripción general

- **Mesa**: lugar físico donde se sientan los clientes.  
- **Cuenta**: registro vivo del consumo de la mesa. Se **abre** cuando el cliente realiza el primer pedido y se va actualizando con más productos.  
- **Venta**: registro final/contable que se genera al **cerrar la cuenta**. Se utiliza para reportes, proyecciones de ventas mensuales, ganancias, etc.  
- **Producto**: ítems del menú (comida, bebida, etc.) que el cliente consume.

---

## 2. Actores

### 2.1 Mesero
- Asigna mesas a clientes.
- Abre cuentas al tomar el primer pedido.
- Registra y modifica pedidos en las cuentas.
- Solicita la cuenta al cajero o al sistema.

### 2.2 Cajero
- Cobra cuentas.
- Genera ventas a partir de cuentas cerradas.
- Apoya en el cierre de día.

### 2.3 Administrador
- Gestiona productos del menú.
- Consulta reportes de ventas y estadísticas.

---

## 3. Lista de casos de uso

1. **UC1 – Asignar mesa a cliente**  
2. **UC2 – Abrir cuenta al tomar el primer pedido**  
3. **UC3 – Registrar productos en una cuenta**  
4. **UC4 – Modificar cuenta (cambiar o eliminar productos)**  
5. **UC5 – Solicitar cuenta al cliente**  
6. **UC6 – Cobrar cuenta y generar venta**  
7. **UC7 – Liberar mesa**  
8. **UC8 – Gestionar productos del menú**  
9. **UC9 – Consultar ventas para reportes mensuales**  
10. **UC10 – Consultar detalle de una venta**

---

## 4. Descripción de casos de uso

### UC1 – Asignar mesa a cliente

- **Actor principal:** Mesero  
- **Entidades:** Mesa  
- **Objetivo:** Marcar una mesa como ocupada por un nuevo grupo de clientes.  

**Descripción breve:**  
El mesero selecciona una mesa disponible en el sistema y la marca como *ocupada*. En esta fase todavía no existe cuenta ni venta, solo se registra que la mesa está en uso.

---

### UC2 – Abrir cuenta al tomar el primer pedido

- **Actor principal:** Mesero  
- **Entidades:** Mesa, Cuenta, Producto  
- **Objetivo:** Crear una cuenta para la mesa cuando el cliente realiza su primer pedido.  

**Flujo básico:**
1. El mesero selecciona una mesa ocupada.
2. El mesero registra el primer producto solicitado.
3. El sistema crea una **cuenta** asociada a la mesa.
4. La cuenta queda en estado **abierta** y se registra el producto como primera línea de consumo.

**Precondiciones:**
- La mesa está en estado *ocupada*.

**Postcondiciones:**
- Existe una cuenta abierta asociada a la mesa.
- El primer producto queda registrado en la cuenta.

---

### UC3 – Registrar productos en una cuenta

- **Actor principal:** Mesero  
- **Entidades:** Cuenta, Producto, Mesa  
- **Objetivo:** Agregar nuevos productos consumidos a la cuenta abierta de la mesa.  

**Flujo básico:**
1. El mesero selecciona la mesa que tiene una cuenta abierta.
2. El sistema muestra el detalle actual de la cuenta.
3. El mesero selecciona uno o más productos del menú y especifica cantidades (y notas si aplica).
4. El sistema agrega las líneas de productos a la cuenta y recalcula el total provisional.

**Precondiciones:**
- La cuenta de la mesa está en estado *abierta*.

**Postcondiciones:**
- La cuenta contiene todos los productos agregados.
- El total de la cuenta se actualiza.

---

### UC4 – Modificar cuenta (cambiar o eliminar productos)

- **Actor principal:** Mesero  
- **Entidades:** Cuenta, Producto  
- **Objetivo:** Ajustar el contenido de la cuenta antes de cerrarla (correcciones de pedido).  

**Flujo básico:**
1. El mesero abre la cuenta asociada a la mesa.
2. El sistema muestra el detalle de productos.
3. El mesero:
   - Cambia cantidades de un producto **y/o**
   - Elimina productos **y/o**
   - Agrega productos adicionales.
4. El sistema actualiza el detalle y recalcula el total.

**Flujos alternos:**
- Si se intenta modificar una cuenta ya cerrada, el sistema muestra un mensaje de error e impide cambios.

---

### UC5 – Solicitar cuenta al cliente

- **Actor principal:** Mesero / Cajero  
- **Entidades:** Cuenta, Mesa  
- **Objetivo:** Presentar al cliente el detalle de su consumo antes del pago.  

**Flujo básico:**
1. El mesero indica que el cliente desea la cuenta.
2. El sistema obtiene la cuenta abierta asociada a la mesa.
3. El sistema muestra o imprime la **cuenta** con los productos, cantidades, precios y total.
4. La cuenta puede pasar a estado *pendiente de pago*.

---

### UC6 – Cobrar cuenta y generar venta

- **Actor principal:** Cajero  
- **Entidades:** Cuenta, Venta, Mesa  
- **Objetivo:** Registrar el pago de la cuenta y generar la venta para fines contables y de reporte.  

**Flujo básico:**
1. El cajero selecciona la cuenta pendiente de pago.
2. El sistema muestra el detalle de la cuenta y el total a pagar.
3. El cajero registra el método de pago y el monto recibido.
4. El sistema calcula el cambio (si aplica) y lo muestra.
5. El sistema marca la **cuenta** como *cerrada/pagada*.
6. El sistema crea u
