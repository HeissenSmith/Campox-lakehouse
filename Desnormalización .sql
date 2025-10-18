CREATE OR REPLACE TABLE `ingdatosurp.dl_csantoyo_staging.Staging_Desnormalizado`
PARTITION BY (fecha_pedido)
CLUSTER BY ID_cliente, codigo_producto
AS
SELECT
    -- Información del Cliente y Empleado
    c.customerNumber AS ID_cliente,
    c.customerName AS nombre_cliente,
    c.contactFirstName AS nombre_contacto,
    c.contactLastName AS apellido_contacto,
    c.phone AS telefono_cliente,
    c.addressLine1 AS direccion_cliente,
    c.city AS ciudad_cliente,
    c.country AS pais_cliente,

    e.employeeNumber AS ID_empleado_venta,
    e.firstName AS nombre_empleado_venta,
    e.lastName AS apellido_empleado_venta,
    e.email AS email_empleado_venta,

    o.city AS ciudad_oficina,
    o.phone AS telefono_oficina,
    o.country AS pais_oficina,

    -- Información del Pedido
    ord.orderNumber AS ID_pedido,
    ord.orderDate AS fecha_pedido,
    ord.requiredDate AS fecha_requerida,
    ord.shippedDate AS fecha_envio,
    ord.status AS estado_pedido,
    ord.comments AS comentarios_pedido,

    -- Información del Producto
    p.productCode AS codigo_producto,
    p.productName AS nombre_producto,
    p.productLine AS linea_producto,
    p.productDescription AS descripcion_producto,
    pl.textDescription AS descripcion_linea_producto,
    p.productVendor AS proveedor_producto,
    p.quantityInStock AS cantidad_en_stock,

    -- Detalles del Pedido y Precios
    od.quantityOrdered AS cantidad_ordenada,
    od.priceEach AS precio_unitario_venta,
    SAFE_MULTIPLY(od.quantityOrdered, od.priceEach) AS total_venta,
    SAFE_SUBTRACT(p.MSRP, p.buyPrice) AS margen_ganancia_unitario,

FROM
    `ingdatosurp.dl_csantoyo_raw.raw_orders` AS ord
LEFT JOIN
    `ingdatosurp.dl_csantoyo_raw.raw_customers` AS c
    ON ord.customerNumber = c.customerNumber
LEFT JOIN
    `ingdatosurp.dl_csantoyo_raw.raw_employees` AS e
    ON c.salesRepEmployeeNumber = e.employeeNumber
LEFT JOIN
    `ingdatosurp.dl_csantoyo_raw.raw_offices` AS o
    ON e.officeCode = o.officeCode
LEFT JOIN
    `ingdatosurp.dl_csantoyo_raw.raw_orderdetails` AS od
    ON ord.orderNumber = od.orderNumber
LEFT JOIN
    `ingdatosurp.dl_csantoyo_raw.raw_products` AS p
    ON od.productCode = p.productCode
LEFT JOIN
    `ingdatosurp.dl_csantoyo_raw.raw_productlines` AS pl
    ON p.productLine = pl.productLine
