// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './components/Home'
import ItemList from './components/ItemList';
import { Helmet } from 'react-helmet';


function App() {
  return (
    <Routes>
    <Route
      path="/"
      element={
        <>
          <Helmet>
            <title>Home Page</title>
            <meta name="og:description" content="hi its my website =)" />
          </Helmet>
          <HomePage />
        </>
      }
    />
    <Route
      path="/ms-upcoming-sales"
      element={
        <>
          <Helmet>
            <title>Upcoming MapleStory Cash Shop Sales</title>
            <meta property="og:title" content="Upcoming MapleStory Cash Shop Sales" />
            <meta property="og:description" content="A tool to see upcoming items going on sale in MapleStory's cash shop!" />
            <meta property="og:image" content="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAlCAYAAAAnQjt6AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAcSSURBVFhHvZhrUFzlHcb3AsvunrPgp07V6bR+6NSpfuk0zrS1Nk2tl7TNxdQGrdrY2rGN1moSIVEZY3O/aYyJJTEYIBcSC6kEMYZIDJAIocAmZINcllu4HAiETWDDHfbp/zks2+zu6TfMO/Obd8/7/7/P85w9Z5c9mCJH2m/VWcJOoUHQZhivkC3MC9oZj72L1CR3quIf8loDk1dNCPhmFmoOe624+KFjULw2Ct8MWv9vfLBIfb69UBmdvGzCxHkTxsuEL2cY0aT2ZJsJV4ptE+K5MWg/NTY9qjjKdyQMTFw2Y+zMrWGi1YwLaY6h1IXq/GAMk+n9Bepz/tq4wGilGSPFtwZ6DdbH4J8L1RyJYGYO884Fav64ZsFwkRnDXxjTecwMzwEzKtLMqM0yoyc/vM5jrrPOPvbfXI9CvOi5a6HqlQwWBrFKkKbxTisGCy2GXD9hgfvgHRi86kYgMIFrl/PhPnA7LudM1TnzmOuss4/93BepdTPjmhW7FqiaZLAxiO29+ao21mrFjQKLIU1HLOioWg+Oq959GL/RipEBL6r234mOoxZ9HhloRmByTOoHMTHUIf1vovGwsd409KS3ZHAwiPPdeao20mDFwHGLIa0SpLn4RT1I27k3UJP3MMb8LfB3FaAs1Q5/9zkJMY6vPnkI7eUp0hWAt3AJvIcs6P/UWJPQk96SwcUgrnd+o2pDnhhcz7MacuWoFaW74tDXdAzD11sx0FWmvx4daJPXp/SAvpYc9DXm6q9ZK91lQ8shK/pyjTUJPektGeIZJH7brxXtRkUMfB9bw+jOtqImzYLKzO/jYvYceHIeFJNs+PuaaI2JsV70NH4qc0dw7YbUs3D+8P3SP1vf59lr0XUitQk96S0ZEhgkYcuvFK3/TCx6s2PC8Oyxor1im36W4cOP/l4vOi9l4ex2ObuWXAxea9bXCOvTg/upE6lN+ktiQe9QkE1zFc1XEIsrh2PCKNpixeTEqMhNwtddF0Vb9QGc2WbFtbZiYKLHsKdP8+g63Vnh2oSe9A4F2fCoovUcs6HrYGwYpzbE6GfV11WH3s6vomh170fJlhj52EqQkW7DHkKd9sxwbUJPeoeCrH1Y0bqOxKIzI5zCtVNButo8hjRWZKBko5xZazHGBzsNewh1WtKi9elJ71CQfzykaO3pNrSlhVPwVqwepKO52pD6snScXherBxnubzfsIdTxpkbr05PeoSCrf6lorbvjEMm5TTYUv/1dnNr8bUMKN9yOMuk5vflbKNp6l2EPKVpjQ/3OaH1C71CQlAcVrVm+JyIpXWeTL6a1/5fq7D+jbF2cPhvVpyl6S4LsiNYn9A4Fef0Xita4w45I8lfG6ZcGGDDkatMJFKbEyVwix4Go+jTUqd8erU/oHQqyao6iNbxtRySfvDoVxHup3JDqwj04+dpUEJ/WYNhDqFO7NVqf0DsUJGm2otVudiCS3FemgtRfLDPk/MndOC4mvY0l6O2oM+wh1KleH61P6B0KsuJnilazwYFIjonA2NA11FWXGuIuSEX+MgniLUFPe61hT03FSeS+HAf3mmh9Qu9QkGUPKJpnjRORnE52oPzDp1FX9bmhSdWJVOT93Y7eBuMgNeWfofCduTj+ih2Vb0brE3qHgrz8U0WrXu2EEZ8vd+DoUjuy/xrNv1+wo2CZA3l/M67nyD7WipMcqEwx1qd3KMhL9zs19+tOXJDmSNxvOFGa7ESRBDolpjfzhXBWTMpXOfWZx5E93Mf91InSFk96h4K8+BOn9uUKRQrRVAmVrykoX6ngXHIEsvafVVN1zjyO7OE+1qkTqX12uQJ6h4Is/bFTy3tOEnKDbLxV5P7JCXqHgjz/I2dj5hNK4MRSaZAwldJUkfT18tlfFKQnKgHxbgoFeXaW4/j7jymjmYkKPv6jgjMrXHCvdsGzPh41W+NRuz1B/lYkoCH1Nnj33IbGvUE+EOSY66zXvZug91/aFI/qNfG4IBruFJdcFpecnIryV1UUvaTi6BIFGYsV7FyojNJ7Okj83O/FvbBqjtPHIOm/u3Ws/LnTR29mYBD+gr57/j32j9Y/ovgzFqvSpGLf418v8jvET096BzPozxR33ZlgTZx7tz0vebbie2+BOrpvsRrISFSR+YQL+5904eDvXTj0lAtZT7tw5BkXPvqDsCQe/xI485jrrLOXezJlf/r0iQlpj6uB7fPUUfla99GLnvQOZtCfsr4h3Cck/uCO2N2P3WuveOaHzrZnZzm1mYSa1KYHvYKe9Naf9PjcqQrfER4Q2LBUWC4kCckzBLWoSW160Iue9NafffkkHiPwzmWBKR8RFgnc8OQMQS1qUpse9KInvfX/BnBMh2E6vlW8bryJ7hHunSGoRU1q04NeYSGmBxf4FvF68ebhncyPFVPPBNSiJrXpQa9gCJPpv2UWjrNwiV2pAAAAAElFTkSuQmCC" />
            <meta property="twitter:title" content="Upcoming MapleStory Cash Shop Sales" />
            <meta property="twitter:description" content="A tool to see upcoming items going on sale in MapleStory's cash shop!" />
            <meta property="twitter:image" content="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACIAAAAlCAYAAAAnQjt6AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAcSSURBVFhHvZhrUFzlHcb3AsvunrPgp07V6bR+6NSpfuk0zrS1Nk2tl7TNxdQGrdrY2rGN1moSIVEZY3O/aYyJJTEYIBcSC6kEMYZIDJAIocAmZINcllu4HAiETWDDHfbp/zks2+zu6TfMO/Obd8/7/7/P85w9Z5c9mCJH2m/VWcJOoUHQZhivkC3MC9oZj72L1CR3quIf8loDk1dNCPhmFmoOe624+KFjULw2Ct8MWv9vfLBIfb69UBmdvGzCxHkTxsuEL2cY0aT2ZJsJV4ptE+K5MWg/NTY9qjjKdyQMTFw2Y+zMrWGi1YwLaY6h1IXq/GAMk+n9Bepz/tq4wGilGSPFtwZ6DdbH4J8L1RyJYGYO884Fav64ZsFwkRnDXxjTecwMzwEzKtLMqM0yoyc/vM5jrrPOPvbfXI9CvOi5a6HqlQwWBrFKkKbxTisGCy2GXD9hgfvgHRi86kYgMIFrl/PhPnA7LudM1TnzmOuss4/93BepdTPjmhW7FqiaZLAxiO29+ao21mrFjQKLIU1HLOioWg+Oq959GL/RipEBL6r234mOoxZ9HhloRmByTOoHMTHUIf1vovGwsd409KS3ZHAwiPPdeao20mDFwHGLIa0SpLn4RT1I27k3UJP3MMb8LfB3FaAs1Q5/9zkJMY6vPnkI7eUp0hWAt3AJvIcs6P/UWJPQk96SwcUgrnd+o2pDnhhcz7MacuWoFaW74tDXdAzD11sx0FWmvx4daJPXp/SAvpYc9DXm6q9ZK91lQ8shK/pyjTUJPektGeIZJH7brxXtRkUMfB9bw+jOtqImzYLKzO/jYvYceHIeFJNs+PuaaI2JsV70NH4qc0dw7YbUs3D+8P3SP1vf59lr0XUitQk96S0ZEhgkYcuvFK3/TCx6s2PC8Oyxor1im36W4cOP/l4vOi9l4ex2ObuWXAxea9bXCOvTg/upE6lN+ktiQe9QkE1zFc1XEIsrh2PCKNpixeTEqMhNwtddF0Vb9QGc2WbFtbZiYKLHsKdP8+g63Vnh2oSe9A4F2fCoovUcs6HrYGwYpzbE6GfV11WH3s6vomh170fJlhj52EqQkW7DHkKd9sxwbUJPeoeCrH1Y0bqOxKIzI5zCtVNButo8hjRWZKBko5xZazHGBzsNewh1WtKi9elJ71CQfzykaO3pNrSlhVPwVqwepKO52pD6snScXherBxnubzfsIdTxpkbr05PeoSCrf6lorbvjEMm5TTYUv/1dnNr8bUMKN9yOMuk5vflbKNp6l2EPKVpjQ/3OaH1C71CQlAcVrVm+JyIpXWeTL6a1/5fq7D+jbF2cPhvVpyl6S4LsiNYn9A4Fef0Xita4w45I8lfG6ZcGGDDkatMJFKbEyVwix4Go+jTUqd8erU/oHQqyao6iNbxtRySfvDoVxHup3JDqwj04+dpUEJ/WYNhDqFO7NVqf0DsUJGm2otVudiCS3FemgtRfLDPk/MndOC4mvY0l6O2oM+wh1KleH61P6B0KsuJnilazwYFIjonA2NA11FWXGuIuSEX+MgniLUFPe61hT03FSeS+HAf3mmh9Qu9QkGUPKJpnjRORnE52oPzDp1FX9bmhSdWJVOT93Y7eBuMgNeWfofCduTj+ih2Vb0brE3qHgrz8U0WrXu2EEZ8vd+DoUjuy/xrNv1+wo2CZA3l/M67nyD7WipMcqEwx1qd3KMhL9zs19+tOXJDmSNxvOFGa7ESRBDolpjfzhXBWTMpXOfWZx5E93Mf91InSFk96h4K8+BOn9uUKRQrRVAmVrykoX6ngXHIEsvafVVN1zjyO7OE+1qkTqX12uQJ6h4Is/bFTy3tOEnKDbLxV5P7JCXqHgjz/I2dj5hNK4MRSaZAwldJUkfT18tlfFKQnKgHxbgoFeXaW4/j7jymjmYkKPv6jgjMrXHCvdsGzPh41W+NRuz1B/lYkoCH1Nnj33IbGvUE+EOSY66zXvZug91/aFI/qNfG4IBruFJdcFpecnIryV1UUvaTi6BIFGYsV7FyojNJ7Okj83O/FvbBqjtPHIOm/u3Ws/LnTR29mYBD+gr57/j32j9Y/ovgzFqvSpGLf418v8jvET096BzPozxR33ZlgTZx7tz0vebbie2+BOrpvsRrISFSR+YQL+5904eDvXTj0lAtZT7tw5BkXPvqDsCQe/xI485jrrLOXezJlf/r0iQlpj6uB7fPUUfla99GLnvQOZtCfsr4h3Cck/uCO2N2P3WuveOaHzrZnZzm1mYSa1KYHvYKe9Naf9PjcqQrfER4Q2LBUWC4kCckzBLWoSW160Iue9NafffkkHiPwzmWBKR8RFgnc8OQMQS1qUpse9KInvfX/BnBMh2E6vlW8bryJ7hHunSGoRU1q04NeYSGmBxf4FvF68ebhncyPFVPPBNSiJrXpQa9gCJPpv2UWjrNwiV2pAAAAAElFTkSuQmCC" />
          </Helmet>
          <ItemList />
        </>
      }
    />
  </Routes>
  );
}

export default App;