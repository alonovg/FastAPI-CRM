$(document).ready(function () {
    $("#login-form").submit(function (event) {
        event.preventDefault();

        var name = $("input[name=name]").val();
        var password = $("input[name=password]").val();

        // Валидация данных
        if (name.trim() === "" || password.trim() === "") {
            // Вывод ошибки, если поля не заполнены
            alert("Please fill in both fields.");
            return; // Прерываем выполнение дальнейшего кода
        }

        var data = {
            "name": name,
            "password": password
        };

        $.ajax({
            type: "POST",
            url: "/auth/login",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (response) {
                // Обработка успешного ответа
                window.location.href = "/pages/orders";
            },
            error: function (error) {
                // Обработка ошибки
            }
        });
    });
});
