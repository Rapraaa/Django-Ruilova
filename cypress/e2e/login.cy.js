describe("Modulo de autenticacion", () => {
    beforeEach(() => {
        cy.visit("/");
    });
    it("login fallido", () => {
        //Deberia mostrar un inicio de sesion fallido
        cy.wait(1000);
        cy.contains("Ingresar").click();
        cy.wait(1000);
        cy.get("input#id_username").type("pepitoelmascapito");
        cy.get("input#id_password").type(123456);
        cy.wait(1000);
        cy.contains("Entrar").click();
        cy.contains("Error: Usuario o contraseña incorrectos.");
    });
    it("no debería permitir el registro si la confirmación de contraseña es incorrecta", () => {
        //Fallo en la confirmacion de contrasella
        cy.wait(1000);
        cy.contains("Registrarse").click();
        cy.wait(1000);
        cy.get("input#id_username").type("Prueba1");
        cy.get("input#id_password1").type("123456hola");
        cy.get("input#id_password2").type("123456hola1");
        cy.get("button.btn.btn-custom.btn-lg.shadow").click();
        cy.wait(1500);
        cy.contains("The two password fields didn’t match.");
    });

    it("registro exitoso y login de usuario", () => {
        //Reggistra un usuario valido, para evitar repetir usamos timestamps
        //tambien se puede borrar el usuario previamente o usar una
        //base de datos de prueba
        //const declara variables permanentes, osea que no varian xd
        const ID_unico = Date.now(); //devuelme los milisegundos que han pasado
        //desde del 1 de enero de 1970, a saber pq xd
        cy.wait(1000);
        cy.contains("Registrarse").click();
        cy.wait(1000);
        cy.get("input#id_username").type(`usuario_${ID_unico}`); //es como un fstring
        //SE DEBE USAR COMILLA INVERTIDA
        cy.get("input#id_password1").type("123456hola");
        cy.get("input#id_password2").type("123456hola");
        cy.get("button.btn.btn-custom.btn-lg.shadow").click();
        cy.wait(1000);
        cy.contains(`usuario_${ID_unico}`);
        cy.contains("Salir").click();
        cy.wait(1500);
        cy.get("input#id_username").type(`usuario_${ID_unico}`);
        cy.get("input#id_password").type("123456hola");
        cy.contains("Entrar").click();
        cy.wait(1000);
        cy.contains(`usuario_${ID_unico}`);
    });
});

describe("modulo de permisos", () => {
    describe("Usuario no autenticado", () => {
        beforeEach(() => {
            cy.visit("/");
        });
        it("debería redirigir al login cuando un usuario anónimo intenta crear un préstamo", () => {
            cy.wait(1000);
            cy.contains("Solicitar").click();
            cy.wait(500);
            cy.url().should("include", "/login");
            cy.visit("/");
            cy.get(":nth-child(4) > .nav-link").click();
            cy.url().should("include", "/login");
        });

        it("debería redirigir a la pagina de los libros al hacer click en ver libros, en la pagina principal y la barra de arriba", () => {
            cy.wait(1000);
            cy.get(":nth-child(1) > .dashboard-card > .btn").click();
            cy.wait(500);
            cy.url().should("include", "/libros");
            cy.visit("/");
            cy.get(":nth-child(2) > .nav-link").click();
            cy.url().should("include", "/libros");
        });

        it("no deberia poder acceder a crear libros, debe pedir autentificacion", () => {
            cy.visit("/libros/nuevo");
            cy.url().should("include", "/login");
        });
    });
});
