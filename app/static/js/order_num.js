$(document).ready(function () {
    // Находим кнопку "Изменить" - Инфо по заявке, по идентификатору
    var updateOrderBtn = $("#updateOrderBtn");

    // Находим кнопку "Сохранить" инфо по заявке по идентификатору
    var sendUpdateOrderBtn = $("#sendUpdateOrderBtn");

    // // Находим кнопку "Изменить" - Инфо по исполнителю, по идентификатору
    // var updateExecutorBtn = $("#updateExecutorBtn");
    //
    // // Находим кнопку "Сохранить" инфо по заявке по идентификатору
    // var sendUpdateExecutorBtn = $("#sendUpdateExecutorBtn");

    // Находим поля по идентификаторам - заявка
    var orderNameInput = $("#orderNameInput");
    var orderSumInput = $("#orderSumInput");
    var orderPaysSelect = $("#orderPaysSelect");
    var orderStatusSelect = $("#orderStatusSelect");
    var orderGetPaySelect = $("#orderGetPaySelect");


    // Находим поля по идентификаторам - исполнитель
    var executorNameInput = $("#executorNameInput");
    var executorSumInput = $("#executorSumInput");
    var executorPaysSelect = $("#executorPaysSelect");
    var executorSendPaySelect = $("#executorSendPaySelect");
    var executorStatusSelect = $("#executorStatusSelect");
    var executorOrderId = $("#executorOrderId");
    var executorOrderNum = $("#executorOrderNum");

    // Устанавливаем начальное состояние полей (заблокированными) - order
    orderNameInput.prop("disabled", true);
    orderSumInput.prop("disabled", true);
    orderPaysSelect.prop("disabled", true);
    orderStatusSelect.prop("disabled", true);
    orderGetPaySelect.prop("disabled", true);

    // Устанавливаем начальное состояние полей (заблокированными) - executor
    executorNameInput.prop("disabled", true)
    executorSumInput.prop("disabled", true)
    executorPaysSelect.prop("disabled", true)
    executorSendPaySelect.prop("disabled", true)
    executorStatusSelect.prop("disabled", true)

    var currentValueExecutorSum = executorSumInput.val();
    if (currentValueExecutorSum === "None") {
        // Если значение None, устанавливаем текст на "0 ₽."
        executorSumInput.val("0 ₽.")
    }

    var currentValue = orderSumInput.val();
    if (currentValue === "None") {
        // Если значение None, устанавливаем текст на "0 ₽."
        orderSumInput.val("0 ₽.");
    }

    // Добавляем обработчик события на клик по кнопке "Изменить"
    updateOrderBtn.click(function () {
        // При нажатии на кнопку, разблокируем поля - Order
        orderNameInput.prop("disabled", false);
        orderSumInput.prop("disabled", false);
        orderPaysSelect.prop("disabled", false);
        orderStatusSelect.prop("disabled", false);
        orderGetPaySelect.prop("disabled", false);
    });

    $(".update-executor-btn").click(function () {
        var executorId = $(this).data("executor-id");
        // Ваши действия для кнопки "Изменить" здесь, используя executorId

        // Блокируем соответствующие поля - Executor
        $(".executor-name-input[data-executor-id='" + executorId + "']").prop("disabled", false)
        $(".executor-sum-input[data-executor-id='" + executorId + "']").prop("disabled", false);
        $(".executor-pays-select[data-executor-id='" + executorId + "']").prop("disabled", false);
        $(".executor-send-pay-select[data-executor-id='" + executorId + "']").prop("disabled", false);
        $(".executor-status-select[data-executor-id='" + executorId + "']").prop("disabled", false);
    });

    // updateExecutorBtn.click(function () {
    //     // При нажатии на кнопку, разблокируем поля - Executor
    //     executorSumInput.prop("disabled", false);
    //     executorPaysSelect.prop("disabled", false);
    //     executorSendPaySelect.prop("disabled", false);
    //     executorStatusSelect.prop("disabled", false);
    // });

    // Добавляем обработчик события на клик по кнопке "Сохранить" - executor
    $(".send-update-executor-btn").click(function () {
        var executorId = $(this).data("executor-id");
        // Ваши действия для кнопки "Сохранить" здесь, используя executorId

        // Получаем значения полей для данного исполнителя
        var executorNameInput = $(".executor-name-input[data-executor-id='" + executorId + "']").val();
        var executorSumInput = $(".executor-sum-input[data-executor-id='" + executorId + "']").val();
        var executorPaysSelect = $(".executor-pays-select[data-executor-id='" + executorId + "']").val();
        var executorSendPaySelect = $(".executor-send-pay-select[data-executor-id='" + executorId + "']").val();
        var executorStatusSelect = $(".executor-status-select[data-executor-id='" + executorId + "']").val();
        var executorOrderId = $(".executor-order-id[data-executor-id='" + executorId + "']").val();

        // Разблокируем соответствующие поля - Executor
        $(".executor-name-input[data-executor-id='" + executorId + "']").prop("disabled", true);
        $(".executor-sum-input[data-executor-id='" + executorId + "']").prop("disabled", true);
        $(".executor-pays-select[data-executor-id='" + executorId + "']").prop("disabled", true);
        $(".executor-send-pay-select[data-executor-id='" + executorId + "']").prop("disabled", true);
        $(".executor-status-select[data-executor-id='" + executorId + "']").prop("disabled", true);

        // Удаляем символы " ₽." и преобразуем в число
        executorSumInput = parseFloat(executorSumInput.replace(" ₽.", ""));

        // Создаем объект данных для отправки
        var data_executor = {
            "order_name": executorNameInput,
            "order_id": executorOrderId,
            "order_sum": executorSumInput,
            "order_status": executorStatusSelect,
            "order_pay_method": executorPaysSelect,
            "order_send_pay": executorSendPaySelect
        };

        // Отправляем POST-запрос на сервер
        $.post("/performers/update/executor-info", data_executor, function (response) {
            // Обработка ответа от сервера (если необходимо)
            console.log(response);
            if (response.status === 200) {
                location.reload(); // Перезагрузка текущей страницы
            }
        });
    });

    // Добавляем обработчик события на клик по кнопке "Сохранить" - executor
    // sendUpdateExecutorBtn.click(function () {
    //     var executorSumInput = $("#executorSumInput" + executorId).val();
    //     var executorPaysSelect = $("#executorPaysSelect" + executorId).val();
    //     var executorSendPaySelect = $("#executorSendPaySelect" + executorId).val();
    //     var executorStatusSelect = $("#executorStatusSelect" + executorId).val();
    //     var executorOrderId = $("#executorOrderId").val();
    //
    //     // Удаляем символы " ₽." и преобразуем в число
    //     executorSumInput = parseFloat(executorSumInput.replace(" ₽.", ""));
    //
    //     // Создаем объект данных для отправки
    //     var data_executor = {
    //         "order_id": executorOrderId,
    //         "order_sum": executorSumInput,
    //         "order_status": executorStatusSelect,
    //         "order_pay_method": executorPaysSelect,
    //         "order_send_pay": executorSendPaySelect
    //     };
    //
    //     // Отправляем POST-запрос на сервер
    //     $.post("/performers/update/executor-info", data_executor, function (response) {
    //         // Обработка ответа от сервера (если необходимо)
    //         console.log(response);
    //         if (response.status === 200) {
    //             location.reload(); // Перезагрузка текущей страницы
    //         }
    //     });
    // });

    // Добавляем обработчик события на клик по кнопке "Сохранить" - order
    sendUpdateOrderBtn.click(function () {
        // Получаем значения полей
        var orderName = $("#orderNameInput").val();
        var orderSum = $("#orderSumInput").val();
        var orderPays = $("#orderPaysSelect").val();
        var orderStatus = $("#orderStatusSelect").val();
        var orderGetPay = $("#orderGetPaySelect").val();
        var orderPageNum = $("#orderPageNum").val();
        var orderIdSelect = $("#orderIdSelect").val();

        // Удаляем символы " ₽." и преобразуем в число
        orderSum = parseFloat(orderSum.replace(" ₽.", ""));

        // Создаем объект данных для отправки
        var data = {
            "order_name": orderName,
            "order_status": orderStatus,
            "order_get_pay": orderGetPay,
            "order_sum": orderSum,
            "order_pay_method": orderPays,
            "order_num": orderPageNum,
            "order_id": orderIdSelect
        };

        // Отправляем POST-запрос на сервер
        $.post("/orders/update/order_info", data, function (response) {
            // Обработка ответа от сервера (если необходимо)
            console.log(response);
            if (response.status === 200) {
                location.reload(); // Перезагрузка текущей страницы
            }
        });
    });
});
