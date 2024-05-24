variable "main_region" {
  type        = string
  description = "The main location for the resources."
}

variable "team_ids" {
  type        = list(string)
  description = "The principal ids of the technical team."
  default     = []
}

variable "admin_ids" {
  type        = list(string)
  description = "The principal ids of the admins."
  default     = []
}

variable "team_emails" {
  type        = list(string)
  description = "The emails of the team."
  default     = []
}