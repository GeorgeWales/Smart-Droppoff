//
//  ViewController.swift
//  Smart-Dropoff
//
//  Created by George Wales on 27/02/2025.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var Username: UITextField!
    @IBOutlet weak var Password: UITextField!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }
    
    @IBAction func LoginBtn(_ sender: UIButton) {
        let username = Username.text ?? ""
        let password = Password.text ?? ""
        
        if username.isEmpty || password.isEmpty{
            showAlert(title: "Error", message: "Please enter Username and Password")
            return
        }
        
        login(username: username, password: password)
        
    }
    func login(username: String, password: String) {
            guard let url = URL(string: "http://localhost:4001/login") else { return } // Update this URL when Flask is deployed
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")

            let postData = ["username": username, "password": password]
            request.httpBody = try? JSONSerialization.data(withJSONObject: postData)

            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                guard let data = data, error == nil else {
                    DispatchQueue.main.async {
                        self.showAlert(title: "Error", message: "Network error: \(error?.localizedDescription ?? "Unknown error")")
                    }
                    return
                }

                if let json = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: String] {
                    DispatchQueue.main.async {
                        if json["status"] == "success" {
                            self.showAlert(title: "Success", message: "Login successful! 🎉")
                            // take to next page
                        } else {
                            self.showAlert(title: "Login Failed", message: json["message"] ?? "Unknown error")
                        }
                    }
                }
            }
            task.resume()
        }

        func showAlert(title: String, message: String) {
            let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
            alert.addAction(UIAlertAction(title: "OK", style: .default))
            present(alert, animated: true)
        }
    }

