console.log("Inventory system loaded");

// Product search filter
document.addEventListener("DOMContentLoaded",function ()
{
    const searchInput = document.getElementById("productSearch");
    const rows = document.querySelectorAll(".product-row");
    if (searchInput) {
        searchInput.addEventListener("keyup",function (){
            const value = this.value.toLowerCase();
            rows.forEach(row => {
                const name = row.querySelector(".p-name").innerText.toLowerCase();
                const brand = row.querySelector(".p-brand").innerText.toLowerCase();
                row.computedStyleMap.display = name.includes(value) || brand.includes(value) ?"":"none";
            });
        });
    }
    document.querySelectorAll(".item-check").forEach(check => {
        check.addEventListener("change",function ()
    {
        const id = this.dataset.id;
        const qtyInput = document.querySelector('.qty-input[data-id="${id}"]');
        if (this.checked) {
            qtyInput.disabled = false;
            qtyInput.focus();
        }else{
            qtyInput.value = 0;
            qtyInput.disabled = true;
        }
    });
    });
});
document.addEventListener("DOMContentLoaded", () => {

  const cart = {};
  const cartTable = document.getElementById("cartTable");
  const totalAmountEl = document.getElementById("totalAmount");
  const totalProfitEl = document.getElementById("totalProfit");

  // 🔍 Product search
  const search = document.getElementById("searchProduct");
  search.addEventListener("keyup", () => {
    const val = search.value.toLowerCase();
    document.querySelectorAll(".product-item").forEach(p => {
      p.style.display =
        p.dataset.name.includes(val) || p.dataset.brand.includes(val)
          ? "" : "none";
    });
  });

  // ➕ Add to cart
  document.querySelectorAll(".add-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;
      if (!cart[id]) {
        cart[id] = {
          name: btn.dataset.name,
          price: parseFloat(btn.dataset.price),
          profit: parseFloat(btn.dataset.profit),
          qty: 1,
          stock: parseInt(btn.dataset.stock)
        };
      } else if (cart[id].qty < cart[id].stock) {
        cart[id].qty++;
      }
      renderCart();
    });
  });

  // 🔄 Render cart
  function renderCart() {
    cartTable.innerHTML = `
      <tr><th>Item</th><th>Qty</th><th>Total</th><th></th></tr>
    `;

    let total = 0, profit = 0;

    Object.keys(cart).forEach(id => {
      const item = cart[id];
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${item.name}</td>
        <td>
          <input type="number" min="1" max="${item.stock}"
                 name="qty_${id}"
                 value="${item.qty}"
                 class="form-control qty-field">
        </td>
        <td>₹${item.qty * item.price}</td>
        <td>
          <button type="button" class="btn btn-sm btn-danger remove-btn">❌</button>
        </td>
      `;

      row.querySelector(".qty-field").addEventListener("change", e => {
        const v = parseInt(e.target.value);
        if (v > 0 && v <= item.stock) {
          item.qty = v;
          renderCart();
        }
      });

      row.querySelector(".remove-btn").addEventListener("click", () => {
        delete cart[id];
        renderCart();
      });

      cartTable.appendChild(row);

      total += item.qty * item.price;
      profit += item.qty * item.profit;
    });

    totalAmountEl.innerText = total;
    totalProfitEl.innerText = profit;
  }

});
