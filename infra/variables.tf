variable "project_name" {
  type        = string
  default     = "transcription-demo"
  description = "Project name"
}

variable "location" {
  type        = string
  default     = "westeurope"
  description = "Resource group location"
}

variable "openai_api_key" {
  type        = string
}

variable "huggingface_token" {
  type        = string
}

variable "cohere_api_key" {
  type        = string
}

variable "torch_device" {
  type        = string
}

variable "azure_search_endpoint" {
  type        = string
}

variable "azure_search_key" {
  type        = string
}

variable "azure_search_index_name" {
  type        = string
}
