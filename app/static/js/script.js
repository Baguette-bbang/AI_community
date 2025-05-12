// DOM이 완전히 로드된 후 실행
document.addEventListener("DOMContentLoaded", function () {
  // 부트스트랩 툴팁 초기화
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // 플래시 메시지 자동 닫기 (5초 후)
  setTimeout(function () {
    var alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
      var bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);

  // 모바일 메뉴 닫기 (메뉴 항목 클릭 시)
  var navLinks = document.querySelectorAll(".navbar-nav .nav-link");
  var navbarCollapse = document.querySelector(".navbar-collapse");

  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      if (navbarCollapse.classList.contains("show")) {
        var bsCollapse = new bootstrap.Collapse(navbarCollapse);
        bsCollapse.toggle();
      }
    });
  });
});
