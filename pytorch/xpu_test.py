import argparse
import torch

def test_random_multiplication():
    x = torch.rand(1, 1).to('xpu', dtype=torch.float16)
    y = torch.rand(1, 1).to('xpu', dtype=torch.float16)
    z = x * y
    print("Random FP16 multiplication:")
    print("  Input x:", x.cpu())
    print("  Input y:", y.cpu())
    print("  Output z:", z.cpu())

def test_specific_multiplication():
    x = torch.tensor([[1.0, 2.0]]).to('xpu', dtype=torch.float16)
    y = torch.tensor([[3.0, 4.0]]).to('xpu', dtype=torch.float16)
    z_expected = torch.tensor([[3.0, 8.0]]).to('xpu', dtype=torch.float16)
    z = x * y
    print("Specific FP16 multiplication:")
    print("  Input x:", x.cpu())
    print("  Input y:", y.cpu())
    print("  Output z:", z.cpu())
    if torch.allclose(z, z_expected):
        print("Calculation is correct")
    else:
        print("Calculation is incorrect")

def main(args):
    try:
        # Set random seed for reproducibility
        torch.manual_seed(args.seed)
        import intel_extension_for_pytorch as ipex
        ipex.xpu.seed_all()
        if ipex.xpu.is_available():
            print("Intel XPU device is available")
            device_name = ipex.xpu.get_device_name()
            print("Device name:", device_name)
            if not ipex.xpu.has_fp64_dtype():
                print("Warning: Native FP64 type not supported on this platform")
            # Test random multiplication
            test_random_multiplication()
            # Test specific multiplication
            print("Check if multiplication with two tensors gives expected value")
            test_specific_multiplication()
        else:
            print("Warning: Intel XPU device is not available")
            raise Exception("Intel XPU device not detected")
        print("XPU tests successful!")
    except ImportError as e:
        print("Failed to import Intel Extension for PyTorch:", e)
    except Exception as e:
        print("An error occurred during the test:", e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Intel XPU device')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    args = parser.parse_args()
    main(args)

