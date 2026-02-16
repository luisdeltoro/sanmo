resource "aws_cloudwatch_dashboard" "star-atlas-pricing-dashboard" {
  dashboard_name = "Test_SA_Dashboard"
  dashboard_body = file("${path.module}/sanmo_cw_dashboard.json")
}