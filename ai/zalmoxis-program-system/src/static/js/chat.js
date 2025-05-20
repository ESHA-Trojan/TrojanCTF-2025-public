function getBotResponse() {
  var rawText = $("#textInput").val();
  var sanitizedText = DOMPurify.sanitize(rawText, { ALLOWED_TAGS: [] });
  var userHtml = '<div class="userText"><p>' + sanitizedText + "</p></div>";
  $("#textInput").val("");
  $("#chatbox").append(userHtml);

  document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
  $.get("/alien", { msg: rawText }).done(function (data) {
    var botHtml = '<div class="botText"><p>' + DOMPurify.sanitize(data, { ALLOWED_TAGS: [] });
    +"</p></div>";
    $("#dots").remove();
    $("#chatbox").append(botHtml);
    document.getElementById("userInput").scrollIntoView({ block: "start", behavior: "smooth" });
    $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    $("#textInput").prop("disabled", false).focus();
    $("#textInput").prop("placeholder", "Message");
  });
}

$("#textInput").on("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    rawText = $("#textInput").val();
    var sanitizedText = DOMPurify.sanitize(rawText, { ALLOWED_TAGS: [] });
    if (sanitizedText.trim() === "") {
      return;
    }
    getBotResponse();
    $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    $("#textInput").prop("disabled", true).focus();
    $("#textInput").prop("placeholder", "Wait for the alien to respond...");
    var loadingHtml =
      "<div class='botText typingIndicator' id='dots'>" +
      "<p><span class='dot'/><span class='dot'/><span class='dot'/></p></div>";
    $("#chatbox").append(loadingHtml);
    $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
  }
});
