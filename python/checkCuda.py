import torch

print(torch.version.cuda)
cuda_is_ok = torch.cuda.is_available()
print(f"CUDA Enabled: {cuda_is_ok}")