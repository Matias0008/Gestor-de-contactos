instructions = [
    """
        CREATE TABLE if not exists contacts (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(50) UNIQUE NOT NULL,
            telefono VARCHAR(50) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
    """
]