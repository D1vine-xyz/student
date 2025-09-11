using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace student
{
    class Student
    {
        public int Id { get; set;}
        public string Name { get; set;}
        public int Age { get; set;}
    }
    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = Encoding.UTF8;
            // tao danh sach hoc sinh
            List<Student> students = new List<Student>()
            {
                new Student{ Id = 1, Name = "Tài", Age = 19 },
                new Student{ Id = 2, Name = "Sang", Age = 19 },
                new Student{ Id = 3, Name = "Tiên", Age = 17 },
                new Student{ Id = 4, Name = "Tuấn", Age = 18 },
                new Student{ Id = 5, Name = "Anh", Age = 17 }
            };

            // cau a
            Console.WriteLine("a Danh sach hoc sinh:");
            foreach (var s in students)
            {
                Console.WriteLine($"{s.Id} {s.Name}: {s.Age}");
            }

            // cau b
            Console.WriteLine("\nb Hoc sinh tuoi 15 - 18:");
            var tuoi1518 = students.Where(s => s.Age >= 15 && s.Age <= 18);
            foreach (var s in tuoi1518)
            {
                Console.WriteLine($"{s.Id} {s.Name}: {s.Age}");
            }

            // cau c
            Console.WriteLine("\nc Hoc sinh chu 'A':");
            var tenA = students.Where(s => s.Name.StartsWith("A"));
            foreach (var s in tenA)
            {
                Console.WriteLine($" {s.Name}: {s.Age}");
            }

            // cau d
            Console.WriteLine("\nd Tong tuoi sinh vien:");
            int tongTuoi = students.Sum(s => s.Age);
            Console.WriteLine("Tong so tuoi la = " + tongTuoi);

            // cau e
            Console.WriteLine("\ne Hoc sinh tuoi lon nhat:");
            int maxAge = students.Max(s => s.Age);
            var lonNhat = students.Where(s => s.Age == maxAge);
            foreach (var s in lonNhat)
            {
                Console.WriteLine($"{s.Id} {s.Name}: {s.Age}");
            }

            // cau f
            Console.WriteLine("\nf Hoc sinh tuoi tang dan:");
            var sapXep = students.OrderBy(s => s.Age);
            foreach (var s in sapXep)
            {
                Console.WriteLine($"{s.Id} {s.Name}: {s.Age}");
            }
            Console.ReadLine();
        }
    }
}
